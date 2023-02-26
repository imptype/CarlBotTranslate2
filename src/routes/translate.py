"""
/translate route.
Returns the translation screenshot if successful.
"""

import asyncio
from fastapi import APIRouter, Request, Response
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

router = APIRouter()

@router.get('/translate')
async def translate(request : Request):

  # Get global variables and stuff
  driver = request.app.driver
  cache = request.app.cache
  stats = request.app.stats
  lock = request.app.lock
  configs = request.app.configs
  query = str(request.query_params)
  loop = asyncio.get_event_loop()

  # could check if request from discord/google here BUT makes it 1-3 sec slower

  # Use cache if cached otherwise generate image
  image = cache.get(query)
  if image:
    stats.usecache += 1
  else:
    # Check if request is malformed
    malformed = True
    if request.query_params:
      keys, values = zip(*dict(request.query_params).items())
      if len(keys) == 4 and keys == ('hl', 'sl', 'tl', 'text'):
        if all([1 < len(val) < 6 for val in values[:3]]):
          if not values[3].isspace() and 1 < len(values[3]) < 5000:
            malformed = False
    if malformed:
      stats.malformed += 1
      return 'Request is malformed, import the tag again to fix it.'
    
    # Handle screenshots 1 at a time, queue system
    stats.waiting += 1
    if lock.acquire(timeout = configs['QUEUE_TIMEOUT']):
      stats.waiting -= 1

      # Wrapped in try to make sure lock is released
      try:

        def blocking(): # stuffed selenium code here since most of it is blocking
          
          # Gotos the URL
          driver.get(configs['BASE_URL'] + query)
        
          # Wait for translation to load by checking this element
          element_present = EC.presence_of_element_located((By.CLASS_NAME, configs['CHECK_ELEMENT']))
          try:
            WebDriverWait(driver, 10).until(element_present)
          except: # give up waiting
            stats.skipped += 1
            pass
  
          # Delete some elements
          scripts = ';'.join(
            'try{document.querySelector(".' + e.replace(' ', '.') + '").remove()}catch{}'
            for e in configs['DELETE_ELEMENTS']
          )
          driver.execute_script(scripts)
        
          # Stop loading page
          driver.execute_script('window.stop()')
        
          # Get window size
          width = driver.execute_script('return document.documentElement.scrollWidth')
          height = driver.execute_script('return document.documentElement.scrollHeight')
        
          # Cancel screenshotting operation if its too big, prevents out of memory/crash/timeout
          # Max is around 5000x5000, 25 million pixels
          if width * height > 25000000:
            stats.toobig += 1
            return 1, 'Too big: {}x{}'.format(width, height)
        
          # Update window size if needed
          size = driver.get_window_size()
          changedSize = False
          if width != size['width'] or height != size['height']:
            driver.set_window_size(width, height)
            changedSize = True
        
          # Take screenshot
          image = driver.get_screenshot_as_png()
          
          # Add to cache
          cache[query] = image
        
          # Revert size if changed for future requests
          if changedSize:
            driver.set_window_size(configs['WIDTH'], configs['HEIGHT'])

          return 0, image

        fail, image = await loop.run_in_executor(None, blocking)
        if fail:
          return image # too big text

        stats.success += 1
      except Exception as error:
        stats.failed += 1
        raise error
      finally:
        lock.release()
    
    else:
      stats.waiting -= 1
      stats.timeout += 1
      return 'Request timed out, API is busy right now.'
    
  # Return screenshot
  return Response(image, media_type = 'image/png')
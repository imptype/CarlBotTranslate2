"""
/translate route.
Returns the translation screenshot if successful.
"""

import io
import asyncio
from fastapi import APIRouter, Request, Response

router = APIRouter()+
translator = 

FONT = ImageFont.truetype('arial-unicode.ttf', size = SIZE)
TRANSLATOR = Translator(raise_exception = True)

@router.get('/translate')
async def translate(request : Request):

  # Get global variables and stuff
  driver = request.app.driver
  cache = request.app.cache
  stats = request.app.stats
  semaphore = request.app.semaphore
  translator = request.app.translator
  configs = request.app.configs
  query_dict = dict(request.query_params)
  query_dict.pop('t', None) # discord needs random timestamp/number
  query = urlencode(tuple(query_dict.items()))
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
      keys, values = zip(*query_dict.items())
      if len(keys) == 3 and keys == ('sl', 'tl', 'text'):
        if all([1 < len(val) < 6 for val in values[:2]]):
          if not values[2].isspace() and 1 < len(values[2]) < 4000: # max 4k in discord message
            malformed = False
    if malformed:
      stats.malformed += 1
      return 'Request is malformed, import the tag again to fix it.'
    
    # Handle screenshots with queue system
    stats.waiting += 1
    try:
      await asyncio.wait_for(semaphore.acquire(), configs['TIMEOUT'])
      stats.waiting -= 1

      # Wrapped in try to make sure lock is released
      try:
        
        # Translate first
        text = translator.translate(text, values[1], values[0])

        def blocking(): # blocking pillow code
          # Draw image
          im = Image.new('1', (0, 0))
          draw = ImageDraw.Draw(im)
          left, upper, right, lower = draw.textbbox((0, 0), text, configs['FONT'], spacing = configs['SPACING'])
          height = lower - upper + configs['PADDING'] * 2)
          if height > configs['HEIGHT']:
            height = configs['HEIGHT']
          im = Image.new('1', (right - left + configs['PADDING'] * 2, height, 0)
          draw = ImageDraw.Draw(im)
          draw.text((- left + configd['PADDING'], - upper + configs['PADDING']), text, 1, configs['FONT'], spacing = configs['SPACING'])
          return im.save(io.BytesIO(), 'PNG')

        # Draw image to memory
        image = await loop.run_in_executor(None, blocking)
        stats.success += 1
                         
      except Exception as error:
        stats.failed += 1
        raise error
      finally:
        lock.release()
    
    except asyncio.TimeoutError:
      stats.waiting -= 1
      stats.timeout += 1
      return 'Request timed out, API is busy right now.'
                         
  # Return screenshot
  return Response(image, media_type = 'image/png')

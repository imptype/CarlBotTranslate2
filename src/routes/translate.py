"""
/translate route.
Returns the translation screenshot if successful.
"""

import io
import sys
import asyncio
from urllib.parse import urlencode
from PIL import Image, ImageDraw
from fastapi import APIRouter, Request, Response
from fastapi.responses import FileResponse

router = APIRouter()

@router.get('/translate')
async def translate(request : Request):

  # Get global variables and stuff
  cache = request.app.cache
  stats = request.app.stats
  semaphore = request.app.semaphore
  translator = request.app.translator
  font = request.app.font
  configs = request.app.configs
  query_dict = dict(sorted(request.query_params.items())) # preserve order
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
      if len(query_dict) == 3 and tuple(query_dict) == ('sl', 'text', 'tl'):
        if all(1 < len(query_dict[k]) < 6 for k in ('sl', 'tl')):
          if not query_dict['text'].isspace() and 1 < len(query_dict['text']) < configs['LENGTH']:
            malformed = False
    if malformed:
      stats.malformed += 1
      return FileResponse('src/assets/brokenparams.png')
    
    # Handle image generation with queue system
    stats.waiting += 1
    try:
      await asyncio.wait_for(semaphore.acquire(), configs['TIMEOUT'])
      stats.waiting -= 1

      # Wrapped in try to make sure semaphore is released
      try:
        
        # Translate first
        try:
          text = (await loop.run_in_executor(None, translator.translate, query_dict['text'], query_dict['tl'], query_dict['sl'])).text
        except ValueError as error:
          msg = str(error)
          if msg == 'invalid source language':
            return FileResponse('src/assets/invalidsource.png')
            stats.source += 1
          elif msg == 'invalid destination language':
            stats.target += 1
            return FileResponse('src/assets/invaliddest.png')
          else:
            raise error

        # Adjust if lines overflow max width
        new_lines = []
        lines = text.split('\n')
        space_length = font.getlength(' ')
        for line in lines:
          line_length = font.getlength(line)
          if line_length > configs['WIDTH'] * configs['SCALE']:
            words = line.split(' ')
            line = ''
            line_length = 0 # have to use this, size for fonts are different from len()
            for word in words:
              word_length = font.getlength(word)
              if word_length > configs['WIDTH'] * configs['SCALE']: # case can only be reached intentionally, but sure
                if line and line_length + space_length < configs['WIDTH'] * configs['SCALE']: # otherwise alr on a newline
                  line += ' '
                prev_char = None
                chars = tuple(word)
                for char in chars:
                  if prev_char: # adjust for kerning
                    prev_length = font.getlength(prev_char)
                    two_length = font.getlength(prev_char + char)
                    char_length = two_length - prev_length
                  else:
                    char_length = font.getlength(char)
                  prev_char = char
                  if line_length + char_length > configs['WIDTH'] * configs['SCALE']:
                    new_lines.append(line)
                    line = char
                    line_length = char_length
                  else:
                    line += char
                    line_length += char_length
              # add space if it's not the first word
              elif line_length + space_length * bool(line) + word_length > configs['WIDTH'] * configs['SCALE']:
                new_lines.append(line)
                line = word
                line_length = word_length
              else:
                line += ' ' * bool(line) + word
                line_length += space_length * bool(line) + word_length 
          new_lines.append(line)
        text = '\n'.join(new_lines)

        def blocking(): # blocking pillow code
          # Draw image
          im = Image.new('1', (0, 0))
          draw = ImageDraw.Draw(im)
          left, upper, right, lower = draw.textbbox((0, 0), text, font, spacing = configs['SPACING'])
          height = lower - upper + configs['PADDING'] * configs['SCALE'] * 2
          if height > configs['HEIGHT'] * configs['SCALE'] :
            height = configs['HEIGHT'] * configs['SCALE'] 
          im = Image.new('L', ((right - left + configs['PADDING'] * 2 * configs['SCALE']), height), 0)
          draw = ImageDraw.Draw(im)
          draw.text((- left + configs['PADDING'] * configs['SCALE'], - upper + configs['PADDING'] * configs['SCALE']), text, 255, font, spacing = configs['SPACING'] * configs['SCALE'])
          buffer = io.BytesIO()
          #print('this')
          im.save(buffer, 'PNG')
          #print('that')
          return buffer.getvalue()

        # Draw image to memory
        image = await loop.run_in_executor(None, blocking)

        # Add to cache
        cache[query] = image
        stats.success += 1
      except Exception as error:
        stats.failed += 1
        raise error
      finally:
        semaphore.release()
    
    except asyncio.TimeoutError:
      stats.waiting -= 1
      stats.timeout += 1
      return FileResponse('src/assets/timeout.png')
                         
  # Return screenshot
  stats.transfer += sys.getsizeof(image)
  return Response(image, media_type = 'image/png')

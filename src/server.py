"""
Starts the webserver and inits font and cache.
Also the place where all the configs/constants are stored.
"""

from asyncio import Semaphore
from .classes.ExpiringCache import ExpiringCache
from .classes.Stats import Stats
from .events.middleware import middleware
from .routes import alive, root, translate
from googletrans import Translator
from PIL import ImageFont 
from fastapi import FastAPI

configs = {
  'WIDTH' : 1000, # max width of translated image, excludes padding
  'HEIGHT' : 2000, # max height, in pixels
  'PADDING' : 15, # border padding of image in pixels
  'SPACING' : 0, # spacing between new lines in pixels, default was 4
  'TIMEOUT' : 60 * 2, # 2 mins to queue timeout
  'URL' : 'https://translate.google.com?', # base url
}

def run():
  
  app = FastAPI()
  app.cache = ExpiringCache(60 * 10, 30, 1024 * 1024 * 200) # keep for 10 mins, 30 sec cooldown, max 200 MB
  app.stats = Stats()
  app.semaphore = Semaphore(5) # queue size
  app.configs = configs
  app.translator = Translator(raise_exception = True)
  app.font = ImageFont.truetype('src/assets/Arial-Unicode-MS.ttf', size = 30) # path to ttf and font size
  # this file covers glyphs for all languages decently, a drawback is emojis/special symbols are missing
  # due to max 65k glpyhs in ttf files but unicode has around 150k glyphs, presently pillow can only use 1
  # file at a time, a 'fallback' solution is in progress: https://github.com/python-pillow/Pillow/pull/6926

  app.middleware('http')(middleware) # reverse deco with args

  app.include_router(alive.router)
  app.include_router(root.router)
  app.include_router(translate.router)

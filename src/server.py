"""
Starts the webserver and inits selenium and cache.
Also the place where all the configs/constants are stored.
"""

from asyncio import Semaphore
from .classes.ExpiringCache import ExpiringCache
from .classes.Stats import Stats
from .events.middleware import middleware
from .routes import alive, root, translate
from fastapi import FastAPI

configs = {
  'WIDTH' : 1000, # max width of translated image, excludes padding
  'HEIGHT' : 2000, # max height, in pixels
  'PADDING' : 15, # border padding of image in pixels
  'SPACING' : 0, # spacing between new lines in pixels, default was 4
  'SIZE' : 30, # text/font size
  'TIMEOUT' : 60 * 2, # 2 mins to queue timeout
  'URL' : 'https://translate.google.com?', # base url
}

def run():
  
  app = FastAPI()
  app.cache = ExpiringCache(60 * 10, 30, 1024 * 1024 * 200) # keep for 10 mins, 30 sec cooldown, max 200 MB
  app.stats = Stats()
  app.semaphore = Semaphore(5) # queue size
  app.configs = configs

  app.middleware('http')(middleware) # reverse deco with args

  app.include_router(alive.router)
  app.include_router(root.router)
  app.include_router(translate.router)

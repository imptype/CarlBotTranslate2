"""
Starts the webserver and inits selenium and cache.
Also the place where all the configs/constants are stored.
"""

from asyncio import Lock
from .classes.ChromeDriver import ChromeDriver
from .classes.ExpiringCache import ExpiringCache
from .classes.Stats import Stats
from .events.middleware import middleware
from .routes import alive, root, translate
from fastapi import FastAPI
import uvicorn

configs = {
  'WIDTH' : 1024, 
  'HEIGHT' : 400, #+50 -181 is Y padding without removing below elements
  'BASE_URL' : 'https://translate.google.com?',
  'QUEUE_TIMEOUT' : 60 * 2, # 2 mins to timeout
  'ELEMENT_TIMEOUT' : 20, # 20 seconds to wait for element to appear
  'CHECK_ELEMENT' : 'ryNqvb', # can change in the future, need to update once in a while
  'DELETE_ELEMENTS' : [ # elements to delete that are useless/takes up space
    'asdasd', # test
    'pGxpHc', # Google Translate following banner div
    'VjFXz', # behind banner padding div
    'hgbeOc EjH7wc', # text,images,documents,websites div
    #'zXU7Rb', # Detect Language, English, etc div
    'VlPnLc' # history, saved, contribute div
    ]
}

def run():
  
  app = FastAPI()
  app.driver = ChromeDriver(configs['WIDTH'], configs['HEIGHT'])
  app.cache = ExpiringCache(60 * 10, 30, 1024 * 1024 * 200) # keep for 10 mins, 30 sec cooldown, max 200 MB
  app.stats = Stats()
  app.lock = Lock()
  app.configs = configs

  app.middleware('http')(middleware) # reverse deco with args

  app.include_router(alive.router)
  app.include_router(root.router)
  app.include_router(translate.router)

  uvicorn.run(app, host = '0.0.0.0')

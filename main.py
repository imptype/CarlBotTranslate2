"""
Inits fastapi app, font and cache.
Also the place where all the configs/constants are stored.
"""

from asyncio import Semaphore
from src.classes.ExpiringCache import ExpiringCache
from src.classes.Stats import Stats
from src.events.middleware import middleware
from src.routes import favicon, root, translate
from googletrans import constants, Translator
from PIL import ImageFont 
from fastapi import FastAPI
# import uvicorn

configs = {
  'WIDTH' : 1000, # max width of translated image, excludes padding
  'HEIGHT' : 2000, # max height, in pixels
  'PADDING' : 15, # border padding of image in pixels
  'SPACING' : 0, # spacing between new lines in pixels, default was 4
  'SCALE' : 2, # times to scale up so text is smoother
  'TIMEOUT' : 8, # 8 seconds to queue timeout
  'LENGTH' : 2000, # max characters for text, 2k is max for normal users and tags stop working near 2k anyway
}

constants.LANGUAGES.update({ # add missing languages
  'ckb' : 'Kurdish'
})

app = FastAPI()
app.cache = ExpiringCache(60 * 10, 30, 1024 * 1024 * 200) # keep for 10 mins, 30 sec cooldown, max 200 MB
app.stats = Stats()
app.semaphore = Semaphore(5) # queue size
app.configs = configs
app.translator = Translator(raise_exception = True)
app.font = ImageFont.truetype('src/assets/Arial-Unicode-MS.ttf', size = 30 * configs['SCALE']) # path to ttf and font size
# this file covers glyphs for all languages decently, a drawback is emojis/special symbols are missing
# due to max 65k glpyhs in ttf files but unicode has around 150k glyphs, presently pillow can only use 1
# file at a time, a 'fallback' solution is in progress: https://github.com/python-pillow/Pillow/pull/6926

app.middleware('http')(middleware) # reverse deco with args

app.include_router(favicon.router)
app.include_router(root.router)
app.include_router(translate.router)

# uvicorn.run(app, host = '0.0.0.0')
# you can uncomment this and requirements.txt if you're running from somewhere else
# like repl.it, make sure you do 'pip install -r requirements.txt' to install the libs

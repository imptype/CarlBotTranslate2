"""
/ route.
Contains some quick stats.
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get('/')
async def root(request : Request):
  stats = request.app.stats
  cache = request.app.cache
  semaphore = request.app.semaphore
  return HTMLResponse('<br>'.join([
    'API is online.',
    '',
    'Started: {}'.format(stats.started),
    'Requests: {:,}'.format(stats.requests),
    'Waiting: {:,}'.format(stats.waiting),
    'Timeout: {:,}'.format(stats.timeout),
    'Malformed: {:,}'.format(stats.malformed),
    'Success: {:,}'.format(stats.success),
    'Failed: {:,}'.format(stats.failed),
    'Usecache: {:,}'.format(stats.usecache),
    'Transfer: {:,}'.format(stats.transfer),
    'Cached: {:,}'.format(len(cache)),
    'Size: {:,}'.format(cache._last_bytes),
    'Available: {}'.format(semaphore._value),
    '',
    'Demo: <a href="https://carlbottranslate-1-p5825535.deta.app/">https://carlbottranslate-1-p5825535.deta.app/</a>',
    'Github: <a href="https://github.com/imptype/CarlBotTranslateV2">https://github.com/imptype/CarlBotTranslateV2</a>'
  ]))

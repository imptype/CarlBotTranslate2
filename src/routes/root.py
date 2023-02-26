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
  lock = request.app.lock
  return HTMLResponse('<br>'.join([
    'API is online.',
    '',
    'Started: {}'.format(stats.started),
    'Requests: {:,}'.format(stats.requests),
    'Waiting: {:,}'.format(stats.waiting),
    'Timeout: {:,}'.format(stats.timeout),
    'Skipped: {:,}'.format(stats.skipped),
    'Malformed: {:,}'.format(stats.malformed),
    'Success: {:,}'.format(stats.success),
    'Failed: {:,}'.format(stats.failed),
    'Toobig: {:,}'.format(stats.toobig),
    'Pinged: {:,}'.format(stats.pinged),
    'Usecache: {:,}'.format(stats.usecache),
    'Cached: {:,}'.format(len(cache)),
    'Size: {:,}'.format(cache._last_bytes),
    'Busy: {}'.format(lock.locked()),
    '',
    'Source: <a href="https://replit.com/@imp7/CarlBotTranslate">https://replit.com/@imp7/CarlBotTranslate</a>',
    'Github: <a href="https://github.com/imptype/CarlBotTranslate">https://github.com/imptype/CarlBotTranslate</a>'
  ]))

"""
Currently just a request counter.
"""

from fastapi import Request

async def middleware(request: Request, call_next):
  stats = request.app.stats
  stats.requests += 1
  return await call_next(request)
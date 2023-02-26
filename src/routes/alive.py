"""
/alive[secret] route.
Uptimerobot.com pings this route to keep the repl running mostly 24/7.
According to https://blog.replit.com/glitch, this is not against Replit's ToS.
"""

import os
from fastapi import APIRouter, Request

router = APIRouter()
secret = os.getenv('SECRET')

@router.api_route('/alive{}'.format(secret), methods = ['GET', 'HEAD'])
async def alive(request: Request):  
  stats = request.app.stats
  stats.pinged += 1
  return 'I am alive.'
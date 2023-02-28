"""
The icon on the top left of your browser tab.
"""

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
favicon_path = 'src/assets/favicon.ico'

@router.get('/favicon.ico', include_in_schema = False)
async def favicon():
  return FileResponse(favicon_path)

"""
Modified version of ExpiringCache from R.Danny Bot.
https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/utils/cache.py#L34-L55

Includes:
- Resets TTL per access.
- Min refresh interval, prevents unnecessary refreshing.
- Max bytes (not sure if this is accurate though) + record of it.
"""

import sys
import time

class ExpiringCache(dict):
  def __init__(self, time_to_live, min_interval, max_bytes):
    super().__init__() # as {key : (value, timestamp), etc}
    self.time_to_live = time_to_live
    self.min_interval = min_interval
    self._last_refresh = 0 # used with min_interval
    self.max_bytes = max_bytes
    self._last_bytes = 0 # record of size during last refresh

  def refresh(self): 
    if not self: # empty
      return
    now = time.monotonic()
    if self._last_refresh + self.min_interval > now:
      return
    self._last_refresh = now
    to_remove = []
    self._last_bytes = sys.getsizeof(self)
    for (key, (value, timestamp)) in self.items():
      self._last_bytes += sys.getsizeof(key) + sys.getsizeof(value) + sys.getsizeof(timestamp)
      if now > (timestamp + self.time_to_live):
        to_remove.append(key)
    if self._last_bytes > self.max_bytes:
      return self.clear()
    for key in to_remove: 
      del self[key]
  
  def get(self, key, default = None): # dict.get(...)
    self.refresh()
    value = super().get(key, default)
    if value:
      value = value[0]
      super().__setitem__(key, (value, time.monotonic()))
    return value
    
  def __setitem__(self, key, value): # dict[key] = ...
    self.refresh()
    super().__setitem__(key, (value, time.monotonic())) 
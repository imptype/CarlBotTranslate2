"""
Contains some statistics.
"""

import datetime

class Stats:
  def __init__(self):
    self.started = str(datetime.datetime.utcnow())
    self.requests = 0 # total requests (not just image route)
    self.waiting = 0 # waiting in queue
    self.timeout = 0 # timed out for waiting too long
    self.malformed = 0 # request malformed count
    self.success = 0 # success image request
    self.failed = 0 # image failed request, should record error in deta space logs
    self.usecache = 0 # used from cache count
    self.transfer = 0 # total bytes transferred for success
    self.source = 0 # source error
    self.target = 0 # target error
    # self.unknown for non-discord/google
  
  def __repr__(self):
    return (
      '{}: {:,}'.format(key, val)
      for key, val in self.__dict__.keys()
    )

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
    self.skipped = 0 # skipped waiting when couldn't find element
    self.malformed = 0 # request malformed count
    self.success = 0 # success image request
    self.failed = 0 # image failed request, and hopefully logs to discord.log unless repl.it files fail
    self.toobig = 0 # failed because image too big
    self.pinged = 0 # ping count
    self.usecache = 0 # used from cache count
    # self.unknown for non-discord/google
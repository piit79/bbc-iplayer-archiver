#!/usr/bin/env python

from iplayer.archiver import IPlayerArchiver
from iplayer.episodedb import EpisodeDatabaseJson

db = EpisodeDatabaseJson('database.json')
a = IPlayerArchiver(db, 'episodes', ['b03qkfxh'])
a.run()

#!/usr/bin/env python

import iplayer.archiver as ipa
from pprint import pprint

a = ipa.IPlayerArchiver("database.json", "/home/sedpe03g/src/bbc-iplayer-archiver/episodes", ["b03qkfxh"])

a.run()

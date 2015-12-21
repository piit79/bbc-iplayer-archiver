#!/usr/bin/env python

import iplayer.archiver as ipa
import iplayer.converter as ipc
import iplayer.downloader as ipd
from pprint import pprint

a = ipa.IPlayerArchiver("database.json", "/home/sedpe03g/src/bbc-iplayer-archiver/episodes", ["b03qkfxh"])
a.run()

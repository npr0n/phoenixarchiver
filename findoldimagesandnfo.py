#!/usr/bin/python3

import os

searchdir = "/mnt/naspool/media/porn/movies"

for dir in os.walk(searchdir):
  count = 0
  for f in dir[2]:
    if f.endswith('.nfo'):
      datei = os.path.join(dir[0], os.path.splitext(f)[0])
      if not os.path.exists(datei + ".mp4"):
        print(datei + ".nfo")
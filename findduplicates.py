#!/usr/bin/python3

import os

searchdir = "/mnt/naspool/media/porn/movies"

for dir in os.walk(searchdir):
  count = 0
  for f in dir[2]:
    if f.endswith('.mp4'):
      count = count + 1
  if count > 1:
    print(count, dir[0])

import os
import re
import pathlib
from env import *

# chars that get dropped from strings
invalid_chars = [ "'", '"', ",", ";", ":", "!", "?", "<", ">", "|", "%", "&" ]

# chars that get replaced with underscores
replace_chars = [ " " ]

def normalizeFullPath(path: pathlib.Path):
  p = str(path)
  for char in invalid_chars:
    p = p.replace(char, "")
  for char in replace_chars:
    p = p.replace(char, "_")
  path = pathlib.Path(p)
  return path

def findDirHigherResolution(path: pathlib.Path):
  p = str(path)
  resolutions = [ "720p", "1080p", "2160p" ]
  for res in resolutions:
    if res in p:
      basename = path.name.split(res)[0]
      print(basename, res)

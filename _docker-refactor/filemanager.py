import os
import re
import pathlib
from env import *

# chars that get dropped from strings
invalid_chars = [ "'", '"', ",", ";", ":", "!", "?", "<", ">", "|", "%", "&" ]

# chars that get replaced with underscores
replace_chars = [ " " ]

def normalizeFullPath(path):
  path = pathlib.Path(path)
  p = str(path)
  for char in invalid_chars:
    p = p.replace(char, "")
  for char in replace_chars:
    p = p.replace(char, "_")
  path = pathlib.Path(p)
  return path


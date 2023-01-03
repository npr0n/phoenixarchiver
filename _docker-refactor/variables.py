from time import sleep
import multiprocessing
from typing import NamedTuple


# GLOBAL VARS
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
seleniumhub = 'http://127.0.0.1:4444/wd/hub'
mongoUri = "mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive"
mongoDB = "phoenixarchive"
headless = False
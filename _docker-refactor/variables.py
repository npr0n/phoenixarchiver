#!/usr/bin/python3

import os

# GET ENVIRONMENT VARIABLES
SELENIUM_USERAGENT = os.getenv('SELENIUM_USERAGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'False').lower() in ('true', 't', '1', '0')
SELENIUM_URI = os.getenv('SELENIUM_URI', 'http://127.0.0.1:4444/wd/hub')

MONGODB_URI = os.getenv('MONGODB_URI', "mongodb://phoenixinserter:phoenix@localhost:27107/phoenixarchive")
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', "phoenixarchive")

DISCOVERY_MAXPAGES = int(os.getenv('DISCOVERY_MAXPAGES', "10"))

VERBOSE = os.getenv('VERBOSE', 'True')
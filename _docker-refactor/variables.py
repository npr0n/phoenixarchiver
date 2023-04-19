#!/usr/bin/python3

import os

# GET ENVIRONMENT VARIABLES
SELENIUM_USERAGENT = os.getenv('SELENIUM_USERAGENT', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36')
SELENIUM_HEADLESS = os.getenv('SELENIUM_HEADLESS', 'True').lower() in ('true', 't', '1', '0')
SELENIUM_URI = os.getenv('SELENIUM_URI', 'http://127.0.0.1:4444/wd/hub')

MONGODB_URI = os.getenv('MONGODB_URI', "mongodb://phoenixinserter:phoenix@localhost:27107/phoenixarchive")
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', "phoenixarchive")

DISCOVERY_MAXPAGES = int(os.getenv('DISCOVERY_MAXPAGES', "10"))

VERBOSE = os.getenv('VERBOSE', "True").lower() in ('true', 't', '1', '0')

MEGA_ADUT_U = os.getenv('MEGA_ADUT_U', False)
MEGA_ADUT_P = os.getenv('MEGA_ADUT_P', False)

MEGA_BANG_U = os.getenv('MEGA_BANG_U', False)
MEGA_BANG_P = os.getenv('MEGA_BANG_P', False)

MEGA_BRAZ_U = os.getenv('MEGA_BRAZ_U', False)
MEGA_BRAZ_P = os.getenv('MEGA_BRAZ_P', False)

MEGA_EVIL_U = os.getenv('MEGA_EVIL_U', False)
MEGA_EVIL_P = os.getenv('MEGA_EVIL_P', False)

MEGA_GENX_U = os.getenv('MEGA_GENX_U', False)
MEGA_GENX_P = os.getenv('MEGA_GENX_P', False)

MEGA_KINK_U = os.getenv('MEGA_KINK_U', False)
MEGA_KINK_P = os.getenv('MEGA_KINK_P', False)

MEGA_MILE_U = os.getenv('MEGA_MILE_U', False)
MEGA_MILE_P = os.getenv('MEGA_MILE_P', False)

MEGA_MYLF_U = os.getenv('MEGA_MYLF_U', False)
MEGA_MYLF_P = os.getenv('MEGA_MYLF_P', False)

MEGA_VIXN_U = os.getenv('MEGA_VIXN_U', False)
MEGA_VIXN_P = os.getenv('MEGA_VIXN_P', False)

MEGA_WICK_U = os.getenv('MEGA_WICK_U', False)
MEGA_WICK_P = os.getenv('MEGA_WICK_P', False)

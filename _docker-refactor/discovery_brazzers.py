#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from time import sleep

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.brazzers.com/site/96/brazzers-exxtra",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "brazzersexxtra"
},
{
  "baseUrl": "https://www.brazzers.com/site/90/hot-and-mean",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "hotandmean"
},
{
  "baseUrl": "https://www.brazzers.com/site/81/real-wife-stories",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "realwifestories"
},
{
  "baseUrl": "https://www.brazzers.com/site/78/milfs-like-it-big",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "milfslikeitbig"
},
{
  "baseUrl": "https://www.brazzers.com/site/67/mommy-got-boobs",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "mommygotboobs"
},
{
  "baseUrl": "https://www.brazzers.com/videos/page/1",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers"
},
{
  "baseUrl": "https://www.brazzers.com/series",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers_collections"
}
]



def brazzers_loop(db, driver, site: dict, maxPage: int = 10, scrollOffset: int = 0):
  
  try:
    discover_site(db = db, driver = driver, site = site, maxPage = maxPage, scrollOffset = scrollOffset)
  except:
    print("an error occurred")


def brazzers_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, scrollOffset: int = 50):
  # mongodb connection
  try:
    db = init_db(mongoUri, mongoDB)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    driver = init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless = headless)
  except:
    print("error setting up webdriver")
    return 1
  
  for site in sites:
    try:
      brazzers_loop(db = db, driver = driver, site = site, maxPage = maxPage, scrollOffset = scrollOffset)
    except:
      continue
  
  driver.quit()
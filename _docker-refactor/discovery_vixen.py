#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from time import sleep

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.blacked.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "blacked"
},
{
  "baseUrl": "https://www.blackedraw.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "blackedraw"
},
{
  "baseUrl": "https://www.deeper.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "deeper"
},
{
  "baseUrl": "https://www.slayed.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "slayed"
},
{
  "baseUrl": "https://www.tushy.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "tushy"
},
{
  "baseUrl": "https://www.tushyraw.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "tushyraw"
},
{
  "baseUrl": "https://www.vixen.com/videos",
  "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
  "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
  "method": "XPATH",
  "collection": "vixen",
  "channel": "vixen"
}
]

def vixen_discovery_loop(db, driver, site: dict, maxPage: int = 10, verbose: bool = False):
  
  try:
    discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, verbose = verbose)
  except:
    print("an error occurred")
  

def vixen_discovery_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, verbose: bool = False):
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
      vixen_discovery_loop(db = db, driver = driver, site = site, maxPage = maxPage, verbose = verbose)
    except:
      continue
  
  driver.quit()
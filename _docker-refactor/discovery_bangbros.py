#!/usr/bin/python3

from variables import *
from wdriver import *
from dbase import *

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://bangbros.com/videos/1",
  "resultSearchPattern": "//a[contains(@class, 'thmb_lnk')]",
  "nextPageSearchPattern": "pagination_btn_next",
  "method": "ID",
  "collection": "bangbros",
  "channelSearchPattern": "..//a[contains(@class, 'thmb_mr_lnk')]",
  "channelSearchAttribute": "innerText",
  "dateSearchPattern": "..//span[contains(@class, 'thmb_mr_2')]/span[contains(@class, 'faTxt')]",
  "dateSearchAttribute": "innerText"
}
]


def bangbros_discovery_loop(db, driver, site: dict, maxPage: int = 10):
  
  try:
    discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, scrollOffset = 30)
  except:
    print("an error occurred")
  

def main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, verbose: bool = False):
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
      bangbros_discovery_loop(db = db, driver = driver, site = site, maxPage = maxPage)
    except:
      continue
  
  driver.quit()

if __name__ == "__main__":
  main()
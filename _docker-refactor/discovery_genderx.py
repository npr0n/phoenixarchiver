#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from time import sleep

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.genderxfilms.com/en/videos",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "genderx"
},
{
  "baseUrl": "https://www.genderxfilms.com/en/dvds",
  "resultSearchPattern": "//a[contains(@class, 'DvdThumb-DvdTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "genderx_collections"
}
]




def cookie_warn_close(driver):
  driver.get("https://www.genderxfilms.com/en/videos")
  sleep(10)
  driver.find_element(By.CLASS_NAME, "cookieConsentBtn").click()

def genderx_discovery_loop(db, driver, site: dict, maxPage: int = 10):
  
  try:
    discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, scrollOffset = 200, prenavsleep = 5)
  except:
    print("an error occurred")
  

def genderx_discovery_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1):
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
  
  # cookie closer
  try:
    cookie_warn_close(driver)
  except:
    print("cookie warning closer failed")

  for site in sites:
    try:
      genderx_discovery_loop(db = db, driver = driver, site = site, maxPage = maxPage)
    except:
      continue
  
  driver.quit()
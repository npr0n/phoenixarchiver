#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from time import sleep

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.kink.com/shoots/latest",
  "resultSearchPattern": "//a[@class= 'shoot-link']",
  "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
  "method": "XPATH",
  "collection": "kink"
},
{
  "baseUrl": "https://www.kink.com/shoots/featured",
  "resultSearchPattern": "//a[@class= 'shoot-link']",
  "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
  "method": "XPATH",
  "collection": "kink"
},
{
  "baseUrl": "https://www.kink.com/shoots/partner",
  "resultSearchPattern": "//a[@class= 'shoot-link']",
  "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
  "method": "XPATH",
  "collection": "kink"
}
]




def cookie_warn_close(driver):
  driver.get("https://www.kink.com")
  #sleep(10)
  driver.find_element(By.ID, "ccc-close").click()

def kink_loop(db, driver, site: dict, maxPage: int = 10):
  
  try:
    discover_site(db, driver, site, maxPage)
  except:
    print("an error occurred")
  

def kink_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1):
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
      kink_loop(db = db, driver = driver, site = site, maxPage = maxPage)
    except:
      continue
  
  driver.quit()
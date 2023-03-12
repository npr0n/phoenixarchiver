#!/usr/bin/python3

from variables import *
import wdriver
import dbase
from time import sleep

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.mylf.com/movies?filter=recent&page=0",
  "resultSearchPattern": "//div[@class= 'description']/a[contains(@href, '/movies/')]",
  "nextPageSearchPattern": "//button[contains(@class, 'btnLoad')]",
  "method": "COUNT",
  "splitpattern": "=",
  "collection": "mylf"
}
]

def cookie_warn_close(driver):
  driver.get("https://www.mylf.com")
  sleep(5)
  driver.find_element(By.ID, "cookie-dismiss-button").click()

def mylf_discovery_loop(db, driver, site: dict, maxPage: int = 10, verbose: bool = False):
  
  try:
    wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, verbose = verbose)
  except:
    print("an error occurred")
  

def main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, verbose: bool = False):
  # mongodb connection
  try:
    db = dbase.init_db(mongoUri, mongoDB)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    driver = wdriver.init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless = headless)
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
      mylf_discovery_loop(db = db, driver = driver, site = site, maxPage = maxPage, verbose = verbose)
    except:
      continue
  
  driver.quit()

if __name__ == "__main__":
  main()
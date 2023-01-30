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
  driver.find_element(By.ID, "ccc-close").click()

def kink_main(mongoUri: str, mongoDB: str, site: dict, useragent: str, command_executor: str, driver_iwait: int = 10, headless: bool = True, maxPage: int = 10, initPage: int = 1):
  # mongodb connection
  db = init_db(mongoUri, mongoDB)
  driver = init_driver(useragent, command_executor, driver_iwait, headless = False)
  sleep(10)
  cookie_warn_close(driver)
  sleep(10)
  discover_site(db, driver, site, maxPage)
  driver.quit()


for site in sites:
  kink_main(mongoUri = "MONGODB_URI", mongoDB = "MONGODB_DATABASE", site = site, useragent = "SELENIUM_USERAGENT", command_executor = "SELENIUM_URI", headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES)

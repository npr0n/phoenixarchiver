#!/usr/bin/python3

import sys
sys.path.append("..")
from _00_common._00_10_common import *
from _00_common._00_20_driver import *
from _00_common._00_30_db import *
from _00_common._00_40_logic import *

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


maxPage = 10

def cookie_warn_close(driver):
  ### COOKIE WARNING CLOSE ###
  # try:
    driver.get("https://www.kink.com")
    driver.find_element(By.ID, "ccc-close").click()
  # except:
    # print("could not close cookie warning banner")

def kink_main(mongoUri: str, mongoDB: str, site: dict, useragent: str, command_executor: str, driver_iwait: int = 10, headless: bool = True, maxPage: int = 10, initPage: int = 1):
  # mongodb connection
  db = init_db(mongoUri, mongoDB)
  driver = init_driver(useragent, command_executor, driver_iwait, headless = True)
  sleep(10)
  cookie_warn_close(driver)
  sleep(10)
  discover_site(db, driver, site, maxPage)
  driver.quit()

def add_numbers(number1, site:dict):
  return number1

# for site in sites:
#   kink_main(db, site, useragent, seleniumhub, headless = headless, maxPage = maxPage)

with multiprocessing.Pool() as pool:
  taskitems = [(mongoUri, mongoDB, site, useragent, seleniumhub) for site in sites]
  # print(taskitems)
  pool.starmap(kink_main, taskitems)
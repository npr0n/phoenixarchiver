#!/usr/bin/python3

from variables import *
import wdriver
import dbase
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep

scrapeSites = [
  "genderx"
]

discoverySites = [
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


def discovery(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = discoverySites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1):
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
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, scrollOffset = 200, prenavsleep = 5)
    except:
      continue
  
  driver.quit()

def genderx_scraper(driver, doc, getmaxtries: int = 1, findmaxtries: int = 1, verbose: bool = False, getsleep: int = 3):
  # get page
  for attempt in range(getmaxtries):
    try:
      actors = []
      categories = []
      driver.get(doc['url'])
      if verbose:
        print(doc['url'])
    except TimeoutException:
      print("page timed out")
      sleep(3)
      continue
    else:
      break
  else:
    print("Website timed out several times. Skipping.")
    return 1
      
  # id
  try:
    doc['id'] = wdriver.urlparse(doc['url']).path.rpartition('/')[-1]
  except:
    pass


  # id_2
  try:
    doc['id_2'] = wdriver.urlparse(doc['url']).path.rsplit('/', 2)[-2]
  except:
    pass
  
  # title
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("title", attempt)
      doc['title'] = driver.find_element(By.XPATH, "//h1[contains(@class, 'Title')]").get_attribute("textContent")
    except NoSuchElementException:
      # 404
      return doc
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("date site format", attempt)
      doc['datesite'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Date-TExt']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
      
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%Y-%m-%d').strftime('%y.%m.%d')
  except:
    pass
      
  # poster url
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, "/html/head/meta[@property = 'og:image']").get_dom_attribute("content")
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ActorThumb-Name-Link')]")):
        actors.append(actor.get_attribute("textContent"))
      doc['actors'] = actors
    except NoSuchElementException:
      continue
    else:
      break
  
  # categories
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("categories", attempt)
      for category in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ScenePlayerHeaderDesktop-Categories-Link']")):
        categories.append(category.get_attribute("textContent"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  if verbose:
    print("parsing completed")

  return doc

def scraper(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = scrapeSites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, driver_iwait: int = 10, verbose: bool = False):
  # mongodb connection
  try:
    if verbose:
      print("setting up db connection")
    db = dbase.init_db(mongoUri, mongoDB)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    if verbose:
      print("starting webdriver")
    driver = wdriver.init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless =  headless)
  except:
    print("error setting up webdriver")
    return 1
  
  # cookie closer
  try:
    if verbose:
      print("closing cookie warning")
    cookie_warn_close(driver)
  except:
    print("cookie warning closer failed")

  for site in sites:
    # set mongo collection
    try:
      collection = db[site]
    except:
      print("error accessing database for collection")
      continue

    while True:
      # find database entry without title
      try:
        doc = wdriver.find_one_no_title(collection)
        if verbose:
          if doc == None:
            print("did not find entry without title")
            break
          else:
            print("found entry without title")
            print(doc)
      except:
        break
      
      # scrape page and update doc
      try:
        if doc != None:
          doc = genderx_scraper(driver = driver, doc = doc, verbose = verbose)
        else:
          if verbose:
            print("finished page")
          break
      except:
        print("error parsing page", driver.current_url)
        break

      # update database entry
      try:
        dbase.upsert(collection = collection, doc = doc, key = "_id")
        if verbose:
          print("updated db entry")
      except:
        print("error updating database", collection)
  if verbose:
    print("sleeping for 30s")
    sleep(30)
  
  driver.quit()

if __name__ == "__main__":
  discovery()
  scraper()
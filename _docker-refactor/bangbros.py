#!/usr/bin/python3

from variables import *
import wdriver
import dbase
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
from time import sleep
import poster

scrapeSites = [
  "bangbros"
]

discoverySites = [
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

def poster_downloader(sites = scrapeSites):
  poster.mega_logout()
  poster.mega_login(MEGA_BANG_U, MEGA_BANG_P)
  for site in sites:
    db = dbase.init_db(uri=MONGODB_URI, database=MONGODB_DATABASE)
    coll = db[site]
    poster.collection_poster_downloader(collection=coll)
  poster.mega_logout()

def page_scraper(driver, doc, getmaxtries: int = 1, findmaxtries: int = 1):
  # get page
  for attempt in range(getmaxtries):
    try:
      actors = []
      categories = []
      driver.get(doc['url'])
      if VERBOSE:
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
    doc['id'] = urlparse(doc['url']).path.rpartition('/')[-1]
  except:
    pass

  # id_2
  try:
    doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
  except:
    pass
  
  # title
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("title", attempt)
      doc['title'] = driver.find_element(By.XPATH, "//div[@class= 'ps-vdoHdd']/h1").get_attribute("textContent")
      if doc['title'] == "":
        return doc
    except NoSuchElementException:
      continue
    else:
      break

  # description
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("description", attempt)
      doc['description'] = driver.find_element(By.XPATH, "//div[@class= 'vdoDesc']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
        
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%b %d, %Y').strftime('%y.%m.%d')
  except:
    pass
      
  # poster url
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'vjs-poster']").value_of_css_property('background-image').split('"')[1]
    except NoSuchElementException:
      continue
    else:
      break
  
  # rating
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("rating", attempt)
      doc['rating'] = driver.find_element(By.XPATH, "//div[@class= 'bVdPl_it_like']/div[@class= 'bVdPl_txt']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//div[@class= 'vdoCast']/a")):
        if not "websites" in actor.get_attribute("href"):
          actors.append(actor.get_attribute("textContent"))
      doc['actors'] = actors
    except NoSuchElementException:
      continue
    else:
      break
  
  # categories
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("categories", attempt)
      for category in (driver.find_elements(By.XPATH, "//div[@class= 'vdoTags']/a")):
        categories.append(category.get_attribute("textContent"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  if VERBOSE:
    print("parsing completed")

  return doc


def scraper(sites = scrapeSites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, driver_iwait: int = 10):
  # mongodb connection
  try:
    if VERBOSE:
      print("setting up db connection")
    db = dbase.init_db(MONGODB_URI, MONGODB_DATABASE)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    if VERBOSE:
      print("starting webdriver")
    driver = wdriver.init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless =  headless)
  except:
    print("error setting up webdriver")
    return 1

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
        doc = dbase.find_one_no_title(collection)
        if VERBOSE:
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
          doc = page_scraper(driver = driver, doc = doc)
        else:
          if VERBOSE:
            print("finished page")
          break
      except:
        print("error parsing page", driver.current_url)
        break

      # update database entry
      try:
        dbase.upsert(collection = collection, doc = doc, key = "_id")
        if VERBOSE:
          print("updated db entry")
      except:
        print("error updating database", collection)
  if VERBOSE:
    print("sleeping for 30s")
    sleep(30)
  
  driver.quit()

def discovery(sites = discoverySites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1):
  # mongodb connection
  try:
    db = dbase.init_db(uri=MONGODB_URI, database=MONGODB_DATABASE)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    driver = wdriver.init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless = headless)
  except:
    print("error setting up webdriver")
    return 1

  for site in sites:
    try:
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, scrollOffset = 30)
    except:
      continue
  
  driver.quit()

if __name__ == "__main__":
  discovery()
  scraper()
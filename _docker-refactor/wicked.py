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
  "wicked"
]

discoverySites = [
{
  "baseUrl": "https://www.wicked.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "wicked",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
}
]


def poster_downloader(sites = scrapeSites):
  poster.mega_logout()
  poster.mega_login(MEGA_WICK_U, MEGA_WICK_P)
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
      doc['title'] = driver.find_element(By.XPATH, "//h1[contains(@class, 'ScenePlayerHeaderDesktop-PlayerTitle-Title')]").get_attribute("textContent")
      if "404" in doc['title']:
        return doc
    except NoSuchElementException:
      continue
    else:
      break

  # # description
  # for attempt in range(findmaxtries):
  #   try:
  #     if VERBOSE:
  #       print("description", attempt)
  #     doc['description'] = driver.find_element(By.XPATH, "//span[@class= 'description-text']").get_attribute("innerText")
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("date site format", attempt)
      doc['datesite'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Date-Text')]").get_attribute("innerText")
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
      if VERBOSE:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, "/html/head/meta[@property= 'og:image']").get_attribute("content")
    except NoSuchElementException:
      continue
    else:
      break
  
  # # channel
  # for attempt in range(findmaxtries):
  #   try:
  #     if VERBOSE:
  #       print("channel", attempt)
  #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break
  
  # director
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("director", attempt)
      doc['director'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Director-Text')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # # rating
  # for attempt in range(findmaxtries):
  #   try:
  #     if VERBOSE:
  #       print("rating", attempt)
  #     doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
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
      if VERBOSE:
        print("categories", attempt)
      for category in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ScenePlayerHeaderDesktop-Categories-Link')]")):
        categories.append(category.get_attribute("innerText"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  # collection title
  for attempt in range(findmaxtries):
    try:
      if (doc['title'].split()[-2].lower() == "scene" ):
        doc['collectiontitle'] = doc['title'].rsplit(' - ', 1)[0]
    except:
      continue
    else:
      break
  
  if VERBOSE:
    print("parsing completed")

  return doc


def discovery(sites = discoverySites, driver_iwait: int = 30):
  # mongodb connection
  try:
    db = dbase.init_db(uri=MONGODB_URI, database=MONGODB_DATABASE)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    driver = wdriver.init_driver(command_executor = SELENIUM_URI, useragent = SELENIUM_USERAGENT, driver_iwait = driver_iwait, headless = SELENIUM_HEADLESS)
  except:
    print("error setting up webdriver")
    return 1
  

  for site in sites:
    try:
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = DISCOVERY_MAXPAGES)
    except:
      continue
  
  driver.quit()


def scraper(sites = scrapeSites, driver_iwait: int = 10):
  # mongodb connection
  try:
    if VERBOSE:
      print("setting up db connection")
    db = dbase.init_db(uri=MONGODB_URI, database=MONGODB_DATABASE)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    if VERBOSE:
      print("starting webdriver")
    driver = wdriver.init_driver(command_executor = SELENIUM_URI, useragent = SELENIUM_USERAGENT, driver_iwait = driver_iwait, headless =  SELENIUM_HEADLESS)
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

if __name__ == "__main__":
  discovery()
  scraper()
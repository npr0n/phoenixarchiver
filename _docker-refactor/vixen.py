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

scrapeSites = [
  "vixen"
]

discoverySites = [
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


def page_scraper(driver, doc, getmaxtries: int = 1, findmaxtries: int = 1, verbose: bool = False):
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
      if verbose:
        print("title", attempt)
      doc['title'] = driver.find_element(By.XPATH, "//head/title").get_attribute("innerText")
      if "Page not found" in doc['title']:
        return doc
    except NoSuchElementException:
      continue
    else:
      break

  # description
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("description", attempt)
      doc['description'] = driver.find_element(By.XPATH, "//div[@data-test-component= 'VideoDescription']/p").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("date site format", attempt)
      doc['datesite'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'ReleaseDateFormatted']").get_attribute("textContent")
    except NoSuchElementException:
      continue
    else:
      break
      
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%B %d, %Y').strftime('%y.%m.%d')
  except:
    pass

  # poster URL won't work here since the site loads the images with one time keys
  # # poster url
  # for attempt in range(findmaxtries):
  #   try:
  #     if verbose:
  #       print("posterurl", attempt)
  #     doc['posterurl'] = driver.find_element(By.XPATH, "//video[@class= 'vjs-tech']").get_attribute("poster")
  #   except NoSuchElementException:
  #     try:
  #       if verbose:
  #         print("posterurl2", attempt)
  #       doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'player']/img").get_attribute("src")
  #     except:
  #       continue
  #   else:
  #     break
  
  
  # director
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("director", attempt)
      doc['director'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'DirectorText']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # rating
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("rating", attempt)
      doc['rating'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'RatingNumber']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//div[@data-test-component= 'VideoModels']/a")):
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
      for category in (driver.find_element(By.XPATH, "//html/head/meta[@name= 'keywords']").get_attribute("content").split(', ')):
        categories.append(category.title())
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
          doc = page_scraper(driver = driver, doc = doc, verbose = verbose)
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

def discovery(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = discoverySites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, verbose: bool = False):
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
  
  for site in sites:
    try:
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, navsleep = 1, verbose = verbose)
    except:
      continue
  
  driver.quit()

if __name__ == "__main__":
  discovery()
  scraper()
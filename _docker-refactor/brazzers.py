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
  "brazzers",
  "brazzers_collections"
]

discoverySites = [
{
  "baseUrl": "https://www.brazzers.com/site/96/brazzers-exxtra",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "brazzersexxtra"
},
{
  "baseUrl": "https://www.brazzers.com/site/90/hot-and-mean",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "hotandmean"
},
{
  "baseUrl": "https://www.brazzers.com/site/81/real-wife-stories",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "realwifestories"
},
{
  "baseUrl": "https://www.brazzers.com/site/78/milfs-like-it-big",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "milfslikeitbig"
},
{
  "baseUrl": "https://www.brazzers.com/site/67/mommy-got-boobs",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers",
  "channel": "mommygotboobs"
},
{
  "baseUrl": "https://www.brazzers.com/videos/page/1",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers"
},
{
  "baseUrl": "https://www.brazzers.com/series",
  "resultSearchPattern": "//span/a[contains(@href, '/video/')]",
  "nextPageSearchPattern": "//ul/li/a[text()= '›']/parent::li",
  "nextPageOffset": "50",
  "method": "XPATH",
  "collection": "brazzers_collections"
}
]


def discovery(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = discoverySites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, maxPage = DISCOVERY_MAXPAGES, driver_iwait: int = 30, initPage: int = 1, scrollOffset: int = 50):
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
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, scrollOffset = scrollOffset)
    except:
      continue
  
  driver.quit()

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
      doc['title'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]").get_attribute("textContent")
      if "404" in doc['title']:
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
      doc['description'] = driver.find_element(By.XPATH, "//section/div/p").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("date site format", attempt)
      doc['datesite'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/preceding-sibling::div[1]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
      
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%B %d, %Y').strftime('%y.%m.%d')
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
      doc['rating'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/preceding-sibling::div/span/div/span").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/parent::div/div/span/a")):
        actors.append(actor.get_attribute("innerText").split(',', 1)[0])
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
      for category in (driver.find_elements(By.XPATH, "//div[contains(@style, 'overflow: hidden;')]/div/a")):
        categories.append(category.get_attribute("innerText"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break

  # collection title
  for attempt in range(findmaxtries):
    try:
      h2text = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']/preceding-sibling::div/div/h2").get_attribute("textContent")
      if (h2text.split()[-1].lower() == "episodes" ):
        doc['collectiontitle'] = h2text.rsplit(' ', 1)[0]
    except NoSuchElementException:
      continue
    else:
      break
  
  if VERBOSE:
    print("parsing completed")

  return doc


def scraper(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = scrapeSites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, driver_iwait: int = 10):
  # mongodb connection
  try:
    if VERBOSE:
      print("setting up db connection")
    db = dbase.init_db(mongoUri, mongoDB)
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

if __name__ == "__main__":
  discovery()
  scraper()
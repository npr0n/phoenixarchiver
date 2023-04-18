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
  "milehigh"
]

discoverySites = [
{
  "baseUrl": "https://www.sweetsinner.com/scenes?page=1",
  "resultSearchPattern": "//span/a[contains(@href, '/scene/')]",
  "nextPageSearchPattern": "//a[contains(text(), '›')]",
  "dateSearchPattern": "../../../../div[2]",
  "dateSearchAttribute": "textContent",
  "method": "XPATH",
  "collection": "milehigh",
  "channel": "sweetsinner"
},
{
  "baseUrl": "https://www.sweetheartvideo.com/scenes?page=1",
  "resultSearchPattern": "//span/a[contains(@href, '/scene/')]",
  "nextPageSearchPattern": "//a[contains(text(), '›')]",
  "dateSearchPattern": "../../../../div[2]",
  "dateSearchAttribute": "textContent",
  "method": "XPATH",
  "collection": "milehigh",
  "channel": "sweetheartvideo"
},
{
  "baseUrl": "https://www.realityjunkies.com/scenes?page=1",
  "resultSearchPattern": "//span/a[contains(@href, '/scene/')]",
  "nextPageSearchPattern": "//a[contains(text(), '›')]",
  "dateSearchPattern": "../../../../div[2]",
  "dateSearchAttribute": "textContent",
  "method": "XPATH",
  "collection": "milehigh",
  "channel": "realityjunkies"
},
{
  "baseUrl": "https://www.doghousedigital.com/scenes?page=1",
  "resultSearchPattern": "//span/a[contains(@href, '/scene/')]",
  "nextPageSearchPattern": "//a[contains(text(), '›')]",
  "dateSearchPattern": "../../../../div[2]",
  "dateSearchAttribute": "textContent",
  "method": "XPATH",
  "collection": "milehigh",
  "channel": "doghousedigital"
},
{
  "baseUrl": "https://www.familysinners.com/scenes?page=1",
  "resultSearchPattern": "//span/a[contains(@href, '/scene/')]",
  "nextPageSearchPattern": "//a[contains(text(), '›')]",
  "dateSearchPattern": "../../../../div[2]",
  "dateSearchAttribute": "textContent",
  "method": "XPATH",
  "collection": "milehigh",
  "channel": "familysinners"
}
]

def confirm_age(driver):
  # sleep(3)
  driver.find_element(By.XPATH, "//button/span[contains(text(), 'Enter')]").click()
  # sleep(5)


def poster_downloader(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = scrapeSites):
  poster.mega_logout()
  poster.mega_login(MEGA_MILE_U, MEGA_MILE_P)
  for site in sites:
    db = dbase.init_db(uri=mongoUri, database=mongoDB)
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
  
  # age confirmer
  try:
    if VERBOSE:
      print("confirming age")
    confirm_age(driver)
  except:
    pass
  
  # title
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("title", attempt)
      doc['title'] = driver.find_element(By.XPATH, "/html/head/title").get_attribute("textContent").split("with")[0].rsplit(" ", 1)[0]
      if doc['title'] == '':
        return doc
      if VERBOSE:
        print("title:", doc['title'])
      
      # title may contain quotation marks
      title = doc['title'].split("'")[0].split('"')[0]
      if VERBOSE:
        print(f"Searching for {title}")
    except NoSuchElementException:
      continue
    else:
      break

  # description
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("description", attempt)
      doc['description'] = driver.find_element(By.XPATH, "//div[contains(text(), 'Description')]/..").get_attribute("textContent").split('Description:')[1]
      if VERBOSE:
        print("description:", doc['description'])
    except NoSuchElementException:
      continue
    else:
      break

  # # date (site format)
  # for attempt in range(findmaxtries):
  #   try:
  #     if VERBOSE:
  #       print("date site format", attempt)
  #     doc['datesite'] = driver.find_element(By.XPATH, "//div[contains(text(), 'Release Date')]/..").get_attribute("textContent").split('Release Date:')[1]
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break
      
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%b %d, %Y').strftime('%y.%m.%d')
    if VERBOSE:
      print("dateymd:", doc['dateymd'])
  except:
    pass
      
  # poster url
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, f"//img[contains(@alt, \'{title}\')]").get_attribute("src")
      if VERBOSE:
        print("posterurl:", doc['posterurl'])
    except NoSuchElementException:
      continue
    except:
      print("error parsing posterurl")
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
  
  # # director
  # for attempt in range(findmaxtries):
  #   try:
  #     if VERBOSE:
  #       print("director", attempt)
  #     doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break
  
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
      for actor in driver.find_elements(By.XPATH, f"//*[self::h1 or self::h2][contains(text(), \'{title}\')]/..//a[contains(@href, '/model/')]"):
        actors.append(actor.get_attribute("textContent"))
      doc['actors'] = actors
      if VERBOSE:
        print("actors:", doc['actors'])
    except NoSuchElementException:
      continue
    except:
      print("error parsing actors")
    else:
      break
  
  # categories
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("categories", attempt)
      for category in driver.find_elements(By.XPATH, "//div[contains(text(), 'Categories')]/../a[contains(@href, '/scenes?tags=')]"):
        categories.append(category.get_attribute("textContent"))
      doc['categories'] = categories
      if VERBOSE:
        print("categories:", doc['categories'])
    except NoSuchElementException:
      continue
    except:
      print("error parsing categories")
    else:
      break
  
  if VERBOSE:
    print("parsing completed")

  return doc


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


  for site in sites:
    try:
      driver.get(site['baseUrl'])
      confirm_age(driver)
    except:
      print("error confirming age")
    
    try:
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage, scrollOffset = 100)
    except:
      continue
  
  driver.quit()


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
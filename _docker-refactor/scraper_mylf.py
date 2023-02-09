#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from discovery_mylf import cookie_warn_close
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep

sites = [
  "mylf"
]

def mylf_scraper(driver, doc, getmaxtries: int = 1, findmaxtries: int = 1, verbose: bool = False):
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
  
  # title
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("title", attempt)
      doc['title'] = driver.find_element(By.XPATH, "//head/title").get_attribute("innerText")
      if 'https://www.mylf.com/not-found/' in driver.current_url:
        print("url is invalid (404):", driver.current_url)
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
      doc['description'] = driver.find_element(By.XPATH, "//div[contains(@class, 'sceneDesc')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("date site format", attempt)
      doc['datesite'] = driver.find_element(By.XPATH, "//div[contains(@class, 'sceneDate')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
      
  # date (yy.mm.dd)
  try:
    doc['dateymd'] = datetime.strptime(doc['datesite'], '%m/%d/%Y').strftime('%y.%m.%d')
  except:
    pass
      
  # poster url
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, "//div/stream[@title= 'video-player']").get_dom_attribute("poster")
    except NoSuchElementException:
      continue
    else:
      break
  
  # channel
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("channel", attempt)
      doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'site-name')]/a").get_attribute("href").rsplit('/', 1)[-1]
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//div[contains(@class, 'contentTitle')]/a[@class= 'model-name-link']")):
        actors.append(actor.get_attribute("innerText"))
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
      for category in (driver.find_elements(By.XPATH, "//div[contains(@class, 'tags-container')]/a[contains(@href, '/search')]")):
        categories.append(category.get_attribute("innerText").split(",")[0])
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  if verbose:
    print("parsing completed")

  return doc


def mylf_scraper_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, driver_iwait: int = 10, verbose: bool = False):
  # mongodb connection
  try:
    if verbose:
      print("setting up db connection")
    db = init_db(mongoUri, mongoDB)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    if verbose:
      print("starting webdriver")
    driver = init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless =  headless)
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
        doc = find_one_no_title(collection)
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
          doc = mylf_scraper(driver = driver, doc = doc, verbose = verbose)
        else:
          if verbose:
            print("finished page")
          break
      except:
        print("error parsing page", driver.current_url)
        break

      # update database entry
      try:
        upsert(collection = collection, doc = doc, key = "_id")
        if verbose:
          print("updated db entry")
      except:
        print("error updating database", collection)
  if verbose:
    print("sleeping for 30s")
    sleep(30)
  
  driver.quit()
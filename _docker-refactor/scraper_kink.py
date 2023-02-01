#!/usr/bin/python3

from variables import *
from webdriver import *
from database import *
from discovery_kink import cookie_warn_close
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from time import sleep

sites = [
  "kink"
]

def kink_scraper(driver, doc, getmaxtries: int = 3, findmaxtries: int = 3):
  # get page
  for attempt in range(getmaxtries):
    try:
      actors = []
      categories = []
      driver.get(doc['url'])
    except TimeoutException:
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
      doc['title'] = driver.find_element(By.XPATH, "//head/title").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # description
  for attempt in range(findmaxtries):
    try:
      doc['description'] = driver.find_element(By.XPATH, "//span[@class= 'description-text']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      doc['datesite'] = driver.find_element(By.XPATH, "//span[@class= 'shoot-date']").get_attribute("innerText")
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
      doc['posterurl'] = driver.find_element(By.XPATH, "//video[@class= 'vjs-tech']").get_attribute("poster")
    except NoSuchElementException:
      try:
        doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'player']/img").get_attribute("src")
      except:
        continue
    else:
      break
  
  # channel
  for attempt in range(findmaxtries):
    try:
      doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    except NoSuchElementException:
      continue
    else:
      break
  
  # director
  for attempt in range(findmaxtries):
    try:
      doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # rating
  for attempt in range(findmaxtries):
    try:
      doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      for actor in (driver.find_elements(By.XPATH, "//p[@class= 'starring']/span[contains(@class, 'names')]/a")):
        actors.append(actor.get_attribute("innerText").split(',', 1)[0])
      doc['actors'] = actors
    except NoSuchElementException:
      continue
    else:
      break
  
  # categories
  for attempt in range(findmaxtries):
    try:
      for category in (driver.find_elements(By.XPATH, "//a[@class= 'tag']")):
        categories.append(category.get_attribute("innerText"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  return doc


def kink_scraper_main(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = sites, useragent = SELENIUM_USERAGENT, command_executor = SELENIUM_URI, headless = SELENIUM_HEADLESS, driver_iwait: int = 30):
  # mongodb connection
  try:
    db = init_db(mongoUri, mongoDB)
  except:
    print("error setting up db connection")
    return 1
  
  # webdriver
  try:
    driver = init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless =  headless)
  except:
    print("error setting up webdriver")
    return 1
  
  # cookie closer
  try:
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
      except:
        break
      
      # scrape page and update doc
      try:
        doc = kink_scraper(driver = driver, doc = doc)
      except:
        print("error parsing page")
        break

      # update database entry
      try:
        upsert(collection = collection, object = doc, key = "_id")
      except:
        print("error updating database", collection)

  driver.quit()
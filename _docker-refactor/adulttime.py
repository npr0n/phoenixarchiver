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
  "adulttime"
]

discoverySites = [
{
  "baseUrl": "https://www.devilsfilm.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21sextury.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21naturals.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21sextreme.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.transfixed.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.agentredgirl.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.girlsway.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.joymii.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.moderndaysins.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.disruptivefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channel": "disruptivefilms",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.modeltime.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.isthisreal.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.zerotolerancefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
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
      doc['title'] = driver.find_element(By.XPATH, "//h1[contains(@class, 'Title')]").get_attribute("textContent")
      if "404" in doc['title']:
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
      doc['description'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-DescriptionText-Paragraph')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

  # date (site format)
  for attempt in range(findmaxtries):
    try:
      if verbose:
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
      if verbose:
        print("posterurl", attempt)
      doc['posterurl'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-VideoBackground')]/img").get_attribute("src").split('?')[0]
    except NoSuchElementException:
      continue
    else:
      break
  
  # channel
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("channel", attempt)
      doc['channel'] = doc['url'].split('/video/')[1].split('/')[0]
    except NoSuchElementException:
      continue
    else:
      break
  
  # director
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("director", attempt)
      doc['director'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Director-Text')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break
  
  # # rating
  # for attempt in range(findmaxtries):
  #   try:
  #     if verbose:
  #       print("rating", attempt)
  #     doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
  #   except NoSuchElementException:
  #     continue
  #   else:
  #     break
  
  # actors
  for attempt in range(findmaxtries):
    try:
      if verbose:
        print("actors", attempt)
      for actor in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ActorThumb-Name-Link')]")):
        actors.append(actor.get_attribute("title"))
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
      for category in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ScenePlayerHeaderDesktop-Categories-Link')]")):
        categories.append(category.get_attribute("innerText"))
      doc['categories'] = categories
    except NoSuchElementException:
      continue
    else:
      break
  
  if verbose:
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
      wdriver.discover_site(db = db, driver = driver, site = site, maxPage = maxPage)
    except:
      continue
  
  driver.quit()


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

if __name__ == "__main__":
  discovery()
  scraper()
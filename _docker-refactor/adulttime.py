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
  "adulttime",
  "evilangel",
  "evilangel_collections"
]

discoverySites = [
{
  "baseUrl": "https://www.evilangel.com/en/movies",
  "resultSearchPattern": "//a[contains(@class, 'DvdThumb-DvdTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "evilangel_collections"
},
{
  "baseUrl": "https://www.evilangel.com/en/videos",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent",
  "collection": "evilangel"
},
{
  "baseUrl": "https://www.devilsfilm.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent",
},
{
  "baseUrl": "https://www.21sextury.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.21naturals.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.21sextreme.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.transfixed.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.agentredgirl.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.girlsway.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.joymii.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.moderndaysins.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.disruptivefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channel": "disruptivefilms",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.modeltime.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.isthisreal.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.zerotolerancefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "channelSearchAttribute": "textContent",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.girlfriendsfilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channel": "girlfriendsfilms",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
},
{
  "baseUrl": "https://www.tabooheat.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "method": "XPATH",
  "collection": "adulttime",
  "channel": "tabooheat",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "dateSearchAttribute": "textContent",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]",
  "ratingSearchAttribute": "textContent"
}
]


def poster_downloader(mongoUri = MONGODB_URI, mongoDB = MONGODB_DATABASE, sites = scrapeSites):
  poster.mega_logout()
  poster.mega_login(MEGA_ADUT_U, MEGA_ADUT_P)
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
      if VERBOSE:
        print("description", attempt)
      doc['description'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-DescriptionText-Paragraph')]").get_attribute("innerText")
    except NoSuchElementException:
      continue
    else:
      break

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
      doc['posterurl'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-VideoBackground')]/img").get_attribute("src").split('?')[0]
    except NoSuchElementException:
      continue
    else:
      break
  
  # channel
  for attempt in range(findmaxtries):
    try:
      if VERBOSE:
        print("channel", attempt)
      doc['channel'] = doc['url'].split('/video/')[1].split('/')[0]
    except NoSuchElementException:
      continue
    else:
      break
  
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
        actors.append(actor.get_attribute("title"))
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
  
  if VERBOSE:
    print("parsing completed")

  return doc


def discovery(sites = discoverySites, driver_iwait: int = 30):
  # mongodb connection
  try:
    db = dbase.init_db(MONGODB_URI, MONGODB_DATABASE)
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
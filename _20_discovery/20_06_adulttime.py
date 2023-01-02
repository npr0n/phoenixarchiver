#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.parse import urlparse
from pymongo.mongo_client import MongoClient
import pymongo.errors
from time import sleep
import logging as log

### SITE CONFIG ###
sites = [
{
  "baseUrl": "https://www.genderxfilms.com/en/videos",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "genderx",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.genderxfilms.com/en/dvds",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "genderx_collections",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.devilsfilm.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21sextury.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21naturals.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.21sextreme.com/en/videos/sort/latest/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.transfixed.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.agentredgirl.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.girlsway.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.joymii.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.moderndaysins.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.fantasymassage.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.disruptivefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channel": "disruptivefilms",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.modeltime.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.isthisreal.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
{
  "baseUrl": "https://www.zerotolerancefilms.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "nextPageSearchPattern": "//a[contains(@class, 'next-Link')]",
  "collection": "adulttime",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "dateSearchPattern": "../../..//span[contains(@class, 'SceneDetail-DatePublished-Text')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
}
]


### GLOBAL ###

# selenium chromium
options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36')
driver = webdriver.Remote(command_executor = 'http://127.0.0.1:4444/wd/hub', options=options)
driver.implicitly_wait(3)

# mongodb connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

maxPage = 10

# ids = [urlparse(link).path.rpartition('/')[-1] for link in links]

for site in sites:
  print("working on site:", site['collection'])
  try:
    currentPage = int(site['baseUrl'].rsplit('/', 1)[1])
    print("current page from url")
  except:
    currentPage = 1
  results = []
  links = []
  url = site['baseUrl']
  collection = db[site['collection']]
  pageCounter = 1
  
  try:
    driver.get(url)
  except:
    print("could not get page", url)
    break

  while pageCounter <= maxPage:
    
    try:
      elems = driver.find_elements(By.XPATH, site['resultSearchPattern'])

      for elem in elems:
        result = {}
        result['url'] = elem.get_attribute('href')
        result['id'] = urlparse(result['url']).path.rpartition('/')[-1]
        try:
          if site['channel']:
            result['channel'] = site['channel']
          else: 
            result['channel'] = elem.find_element(By.XPATH, site['channelSearchPattern']).get_attribute('textContent').lower().replace(' ','').replace(',','').replace("'",'').replace('!','').replace('?','')
        except:
          pass
        
        try:
          result['rating'] = elem.find_element(By.XPATH, site['ratingSearchPattern']).get_attribute('textContent')
        except:
          pass
        
        try:
          result['datesite'] = elem.find_element(By.XPATH, site['dateSearchPattern']).get_attribute('textContent')
        except:
          pass
        
        try:
          # update / insert into database
          # print("upserting:", result['url'])
          collection.update_one({"url": result['url']}, {"$set": result}, upsert=True)
        except pymongo.errors.DuplicateKeyError:
          # probably a race condition due to upsert and multiple unique keys
          continue
        

      # print("Found elements on current page:", len(elems))
    except NoSuchElementException:
      print("no such element exception")
      break

    except:
      print("something went wrong with the scene detection")
      break

    try:
      # we need to scroll down since the element cannot be selected otherwise
      
      nextPageElement = driver.find_element(By.XPATH, site['nextPageSearchPattern'])
      # print("found element")
      actions = ActionChains(driver)
      actions.scroll_to_element(nextPageElement)
      actions.perform()
      # print("scrolled down")
    except:
      print("Something went wrong or we've reached the end.")
      break
    
    try:
      nextPageElement.click()
      # print("clicked button")
      pageCounter += 1
    except ElementClickInterceptedException:
      actions = ActionChains(driver)
      actions.scroll_by_amount(0, 150)
      actions.perform()
      sleep(1)
      nextPageElement.click()
      pageCounter += 1

driver.quit()

#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse
from pymongo import MongoClient
import time
from datetime import datetime

### SITE CONFIG ###
kinksites = [
 "kink"
]

vixensites = [
 "vixen"
]

mylfsites = [
 "mylf"
]

devilsfilmsites = [
# "devilsfilm"
]

genderxsites = [
 "genderx"
]

genderxcollections = [
 "genderx_collections"
]

brazzerssites = [
  "brazzers"
]

brazzerscollections = [
  "brazzers_collections"
]

wickedsites = [
  "wicked"
]

### GLOBAL ###
# selenium chromium
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

getmaxtries = 3
findmaxtries = 3
updatemaxnumber = 100

# mongodb connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

# directory for saved images
imagestore = "/mnt/naspool/media/porn/db-imagestore"

### KINK ################################################################
for site in kinksites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

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
        continue
      else:
        break

    # poster download
    for attempt in range(findmaxtries):
      try:
        posterfn = "/kink/" + doc['id'] + os.path.splitext(urlparse(doc['posterurl']).path)[1]
        if not os.path.exists(imagestore + posterfn):
          request.urlretrieve(doc['posterurl'], imagestore + posterfn)
          doc['posterlocation'] = posterfn
          break
        else:
          doc['posterlocation'] = posterfn
          continue
      except:
        continue
        
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


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

### VIXEN ###############################################################
for site in vixensites:
  collection = db['vixen']
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//h1[@data-test-component= 'VideoTitle']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # description
    for attempt in range(findmaxtries):
      try:
        doc['description'] = driver.find_element(By.XPATH, "//div[@data-test-component= 'VideoDescription']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
        doc['datesite'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'ReleaseDateFormatted']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
        
    # date (yy.mm.dd)
    try:
      doc['dateymd'] = datetime.strptime(doc['datesite'], '%B %d, %Y').strftime('%y.%m.%d')
    except:
      pass
        
    # poster download
    for attempt in range(findmaxtries):
      try:
        posterurl = driver.find_element(By.XPATH, "//picture[@data-test-component= 'ProgressiveImageImage']/img").get_attribute("src")
        posterfn = "/vixen/" + doc['id'] + os.path.splitext(urlparse(posterurl).path)[1]
        if not os.path.exists(imagestore + posterfn):
          request.urlretrieve(posterurl, imagestore + posterfn)
          doc['posterlocation'] = posterfn
          break
        else:
          doc['posterlocation'] = posterfn
          continue
      except:
        continue
        
    # channel
    for attempt in range(findmaxtries):
      try:
        doc['channel'] = doc['url'].split('https://www.')[1].split('.com')[0]
      except NoSuchElementException:
        continue
      else:
        break
    
    # director
    for attempt in range(findmaxtries):
      try:
        doc['director'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'DirectorText']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # rating
    for attempt in range(findmaxtries):
      try:
        doc['rating'] = driver.find_element(By.XPATH, "//span[@data-test-component= 'RatingNumber']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//div[@data-test-component= 'VideoModels']/a")):
          actors.append(actor.get_attribute("textContent").split(',', 1)[0])
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        doc['categories'] = driver.find_element(By.XPATH, "//meta[@name= 'keywords']").get_attribute("content").split(', ')
      except NoSuchElementException:
        continue
      else:
        break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    #print(doc)
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

### MYLF ################################################################
for site in mylfsites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

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
        doc['description'] = driver.find_element(By.XPATH, "//div[contains(@class, 'sceneDesc')]").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
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
        doc['posterurl'] = driver.find_element(By.XPATH, "//stream[@title= 'video-player']").get_dom_attribute("poster")
      except NoSuchElementException:
        continue
      else:
        break
        
    # channel
    for attempt in range(findmaxtries):
      try:
        doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'video-page')]//div[contains(@class, 'siteName')]/a").get_attribute("href").rsplit('/', 1)[-1]
      except NoSuchElementException:
        continue
      else:
        break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//div[contains(@class, 'video-page')]//a[contains(@class, 'model-name-link')]")):
          actors.append(actor.get_attribute("innerText").split(',', 1)[0])
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        for category in (driver.find_elements(By.XPATH, "//div[contains(@class, 'tags-container')]/a")):
          categories.append(category.get_attribute("innerText").strip().rstrip(','))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    #print(doc)
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    break
    #time.sleep(3)

### DEVILSFILM ##########################################################
for site in devilsfilmsites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      except dns.resolver.DNSException:
        print("DNS error, waiting for two minutes...")
        time.sleep(120)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//h1[contains(@class, 'Title')]").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # description
    for attempt in range(findmaxtries):
      try:
        doc['description'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-DescriptionText-Paragraph')]").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
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
        doc['posterurl'] = driver.find_element(By.XPATH, "//div[contains(@class, 'ScenePlayerHeaderDesktop-VideoBackground')]/img").get_attribute("src").split('?')[0]
      except NoSuchElementException:
        continue
      else:
        break
        
    # channel
    for attempt in range(findmaxtries):
      try:
        doc['channel'] = doc['url'].split('/video/')[1].split('/')[0]
      except NoSuchElementException:
        continue
      else:
        break
        
    # director
    for attempt in range(findmaxtries):
      try:
        doc['director'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Director-Text')]").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # actors
    for attempt in range(findmaxtries):
      try:
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
        for category in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ScenePlayerHeaderDesktop-Categories-Link')]")):
          categories.append(category.get_attribute("innerText"))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    #print(doc)
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

### GENDERX #############################################################
for site in genderxsites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//div[@id= 'playerTitle']/h1/span").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # # description
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['description'] = driver.find_element(By.XPATH, "//span[@class= 'description-text']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
        doc['datesite'] = driver.find_element(By.XPATH, "//li[@class= 'updatedDate']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (yy.mm.dd)
    try:
      doc['dateymd'] = datetime.strptime(doc['datesite'], '%m-%d-%Y').strftime('%y.%m.%d')
    except:
     pass
    
    # poster url
    for attempt in range(findmaxtries):
      try:
        doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'vjs-poster']").value_of_css_property('background-image').split('"')[1]
      except NoSuchElementException:
        continue
      else:
        break
        
    # channel
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # director
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # rating
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//div[contains(@class, 'sceneColActors')]/a")):
          actors.append(actor.get_attribute("innerText"))
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        for category in (driver.find_elements(By.XPATH, "//div[contains(@class, 'sceneColCategories')]/span[not (@class= 'categorySeparator')]")):
          categories.append(category.get_attribute("innerText"))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break
    
    # collection url
    for attempt in range(findmaxtries):
      try:
        doc['collectionurl'] = driver.find_element(By.XPATH, "//a[contains(@class, 'dvdLink')]").get_attribute("href")
      except NoSuchElementException:
        continue
      else:
        break
    
    # collection title
    for attempt in range(findmaxtries):
      try:
        doc['collectiontitle'] = driver.find_element(By.XPATH, "//a[contains(@class, 'dvdLink')]/img").get_attribute("title")
      except NoSuchElementException:
        continue
      else:
        break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

### GENDERX_COLLECTIONS #################################################
for site in genderxcollections:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//h3[@class= 'dvdTitle']").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # # description
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['description'] = driver.find_element(By.XPATH, "//span[@class= 'description-text']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
        doc['datesite'] = driver.find_element(By.XPATH, "//li[@class= 'updatedDate']").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (yy.mm.dd)
    try:
      doc['dateymd'] = datetime.strptime(doc['datesite'], '%m-%d-%Y').strftime('%y.%m.%d')
    except:
     pass
    
    # poster url
    for attempt in range(findmaxtries):
      try:
        doc['posterurl'] = driver.find_element(By.XPATH, "//img[@class= 'dvdCover']").get_attribute("src").split('?')[0]
      except NoSuchElementException:
        continue
      else:
        break
        
    # channel
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # director
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # rating
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//span[@class= 'slide-title']")):
          actors.append(actor.get_attribute("innerText"))
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        for category in (driver.find_elements(By.XPATH, "//span[@class= 'categoryListing']")):
          categories.append(category.get_attribute("innerText"))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break

    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

### BRAZZERS ############################################################
for site in brazzerssites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # description
    for attempt in range(findmaxtries):
      try:
        doc['description'] = driver.find_element(By.XPATH, "//section/div/p").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
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
        doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'vjs-poster']").value_of_css_property('background-image').split('"')[1]
      except NoSuchElementException:
        continue
      else:
        break
        
    # # channel
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # # director
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # rating
    for attempt in range(findmaxtries):
      try:
        doc['rating'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/preceding-sibling::div/span/div/span").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/parent::div/div/span/a")):
          actors.append(actor.get_attribute("textContent"))
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        for category in (driver.find_elements(By.XPATH, "//div[contains(@style, 'overflow: hidden;')]/div/a")):
          categories.append(category.get_attribute("textContent"))
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


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    # print("Updated", doc['_id'])
    # break
    # time.sleep(3)

### BRAZZERS_COLLECTIONS ################################################
for site in brazzerscollections:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # description
    for attempt in range(findmaxtries):
      try:
        doc['description'] = driver.find_element(By.XPATH, "//section/div/p").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
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
        doc['posterurl'] = driver.find_element(By.XPATH, "//div[@class= 'vjs-poster']").value_of_css_property('background-image').split('"')[1]
      except NoSuchElementException:
        continue
      else:
        break
        
    # # channel
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # # director
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['director'] = driver.find_element(By.XPATH, "//span[@class= 'director-name']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # rating
    for attempt in range(findmaxtries):
      try:
        doc['rating'] = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/preceding-sibling::div/span/div/span").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # actors
    for attempt in range(findmaxtries):
      try:
        for actor in (driver.find_elements(By.XPATH, "//div[@aria-atomic= 'true']//h2[contains(@class, 'font-secondary')]/parent::div/div/span/a")):
          actors.append(actor.get_attribute("textContent"))
        doc['actors'] = actors
      except NoSuchElementException:
        continue
      else:
        break
    
    # categories
    for attempt in range(findmaxtries):
      try:
        for category in (driver.find_elements(By.XPATH, "//div[contains(@style, 'overflow: hidden;')]/div/a")):
          categories.append(category.get_attribute("textContent"))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break
    
    # # collection title
    # for attempt in range(findmaxtries):
    #   try:
    #     h2text = driver.find_element(By.XPATH, "//div[@aria-atomic= 'true']/preceding-sibling::div/div/h2").get_attribute("textContent")
    #     if (h2text.split()[-1].lower() == "episodes" ):
    #       doc['collectiontitle'] = h2text.rsplit(' ', 1)[0]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    # print("Updated", doc['_id'])
    # break
    # time.sleep(3)

### WICKED ##############################################################
for site in wickedsites:
  collection = db[site]
  print("Working on", site)
  # use maximum or while True
  # for number in range(updatemaxnumber):
  while True:
    try:
      doc = collection.find_one({"title": {"$exists": False}})
      print(doc['_id'])
    except:
      print("Did not find dataset without title.")
      break
    

    # get page
    for attempt in range(getmaxtries):
      try:
        actors = []
        categories = []
        driver.get(doc['url'])
      except TimeoutException:
        time.sleep(3)
        continue
      else:
        break
    else:
      print("Website timed out several times. Skipping.")

    # id_2
    try:
      doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    except:
      continue

    # title
    for attempt in range(findmaxtries):
      try:
        doc['title'] = driver.find_element(By.XPATH, "//h1[contains(@class, 'ScenePlayerHeaderDesktop-PlayerTitle-Title')]").get_attribute("textContent")
      except NoSuchElementException:
        continue
      else:
        break

    # # description
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['description'] = driver.find_element(By.XPATH, "//span[@class= 'description-text']").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break

    # date (site format)
    for attempt in range(findmaxtries):
      try:
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
        doc['posterurl'] = driver.find_element(By.XPATH, "/html/head/meta[@property= 'og:image']").get_attribute("content")
      except NoSuchElementException:
        continue
      else:
        break
        
    # channel
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['channel'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-logo')]/a").get_attribute("href").rsplit('/', 1)[-1]
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # director
    for attempt in range(findmaxtries):
      try:
        doc['director'] = driver.find_element(By.XPATH, "//span[contains(@class, 'ScenePlayerHeaderDesktop-Director-Text')]").get_attribute("innerText")
      except NoSuchElementException:
        continue
      else:
        break
    
    # rating
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['rating'] = driver.find_element(By.XPATH, "//div[contains(@class, 'shoot-info')]//span[contains(@class, 'thumb-up-percentage')]").get_attribute("innerText")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # actors
    for attempt in range(findmaxtries):
      try:
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
        for category in (driver.find_elements(By.XPATH, "//a[contains(@class, 'ScenePlayerHeaderDesktop-Categories-Link')]")):
          categories.append(category.get_attribute("innerText"))
        doc['categories'] = categories
      except NoSuchElementException:
        continue
      else:
        break
    
    # collection url
    # for attempt in range(findmaxtries):
    #   try:
    #     doc['collectionurl'] = driver.find_element(By.XPATH, "//a[contains(@class, 'dvdLink')]").get_attribute("href")
    #   except NoSuchElementException:
    #     continue
    #   else:
    #     break
    
    # collection title
    for attempt in range(findmaxtries):
      try:
        if (doc['title'].split()[-2].lower() == "scene" ):
          doc['collectiontitle'] = doc['title'].rsplit(' - ', 1)[0]
      except:
        continue
      else:
        break


    #print(json.dumps(doc, sort_keys=True, ensure_ascii=False, indent=2))
    filter = { '_id': doc['_id']}

    collection.update_one(filter, { '$set': doc })
    #print("Updated", doc['_id'])
    #break
    #time.sleep(3)

driver.quit()
#print (results)
#print("Found a total of ", len(links))
#print(links)
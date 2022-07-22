from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse
import json
from pymongo import MongoClient
from pprint import pprint

### SITE CONFIG ###
sites = [
# {
#   "baseUrl": "https://www.kink.com/shoots/latest",
#   "resultSearchPattern": "//a[@class= 'shoot-link']",
#   "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
#   "collection": "kink"
# },
# {
#   "baseUrl": "https://www.kink.com/shoots/featured",
#   "resultSearchPattern": "//a[@class= 'shoot-link']",
#   "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
#   "collection": "kink"
# },
# {
#   "baseUrl": "https://www.kink.com/shoots/partner",
#   "resultSearchPattern": "//a[@class= 'shoot-link']",
#   "nextPageSearchPattern": "//nav[@class= 'paginated-nav']/ul/li/a/span[text() = 'Next']/parent::a[1]",
#   "collection": "kink"
# },
# {
#   "baseUrl": "https://www.blacked.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.blackedraw.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.deeper.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.slayed.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.tushy.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.tushyraw.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
# {
#   "baseUrl": "https://www.vixen.com/videos",
#   "resultSearchPattern": "//a[@data-test-component= 'TitleLink']",
#   "nextPageSearchPattern": "//a[@data-test-component= 'PaginationNext']",
#   "collection": "vixen"
# },
{
  "baseUrl": "https://www.devilsfilm.com/en/videos/page/1",
  "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
  "countNextPage": True,
  "collection": "devilsfilm",
  "channelSearchPattern": "../../..//a[contains(@class, 'SceneDetail-ChannelName-Link')]",
  "ratingSearchPattern": "../../..//span[contains(@class, 'SceneDetail-RatingPercentage-Text')]"
},
# {
#   "baseUrl": "https://www.genderxfilms.com/en/videos",
#   "resultSearchPattern": "//a[contains(@class, 'imgLink')]",
#   "nextPageSearchPattern": "//a[@aria-label= 'Next']",
#   "collection": "genderx"
# },
# {
#   "baseUrl": "https://www.genderxfilms.com/en/dvds",
#   "resultSearchPattern": "//a[contains(@class, 'imgLink')]",
#   "nextPageSearchPattern": "//a[@aria-label= 'Next']",
#   "collection": "genderx_collections"
# },
# {
#   "baseUrl": "https://www.brazzers.com/site/96/brazzers-exxtra",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": True,
#   "collection": "brazzers",
#   "channel": "brazzersexxtra"
# },
# {
#   "baseUrl": "https://www.brazzers.com/site/90/hot-and-mean",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": False,
#   "collection": "brazzers",
#   "channel": "hotandmean"
# },
# {
#   "baseUrl": "https://www.brazzers.com/site/81/real-wife-stories",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": False,
#   "collection": "brazzers",
#   "channel": "realwifestories"
# },
# {
#   "baseUrl": "https://www.brazzers.com/site/78/milfs-like-it-big",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": False,
#   "collection": "brazzers",
#   "channel": "milfslikeitbig"
# },
# {
#   "baseUrl": "https://www.brazzers.com/site/67/mommy-got-boobs",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": False,
#   "collection": "brazzers",
#   "channel": "mommygotboobs"
# },
# {
#   "baseUrl": "https://www.brazzers.com/videos/page/1",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": True,
#   "collection": "brazzers"
# },
# {
#   "baseUrl": "https://www.brazzers.com/series",
#   "resultSearchPattern": "//div[@aria-atomic = 'true']//span/a",
#   "countNextPage": False,
#   "collection": "brazzers_collections"
# },
# {
#   "baseUrl": "https://www.wicked.com/en/videos/page/1",
#   "resultSearchPattern": "//a[contains(@class, 'SceneThumb-SceneInfo-SceneTitle-Link')]",
#   "countNextPage": True,
#   "collection": "wicked"
# }
]


### GLOBAL ###
# selenium chromium
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)

# mongodb connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

maxPage = 3

# ids = [urlparse(link).path.rpartition('/')[-1] for link in links]

for site in sites:
  try:
    currentPage = int(site['baseUrl'].rsplit('/', 1)[1])
    #print("current page from url")
  except:
    currentPage = 1
  results = []
  links = []
  url = site['baseUrl']
  collection = db[site['collection']]
  pageCounter = 1
    
  while pageCounter <= maxPage:

    pageCounter += 1
    try:
      driver.get(url)
    except:
      print("could not get page", url)
      break
    

    # print("Current page: ", url)
    try:
      elems = driver.find_elements(By.XPATH, site['resultSearchPattern'])
      for elem in elems:
        result = {}
        result['url'] = elem.get_attribute('href')
        result['id'] = urlparse(result['url']).path.rpartition('/')[-1]
        try:
          result['channel'] = elem.find_element(By.XPATH, site['channelSearchPattern']).get_attribute('textContent').lower().replace(' ','')
        except:
          pass
        
        try:
          result['rating'] = elem.find_element(By.XPATH, site['ratingSearchPattern']).get_attribute('textContent')
        except:
          pass
        
        # update / insert into database
        # print("upserting:", result['url'])
        collection.update_one({"url": result['url']}, {"$set": result}, upsert=True)
        

      # print("Found elements on current page:", len(elems))
    except NoSuchElementException:
      print("no such element exception")
      break

    try:
      try:
        nextPageLink = driver.find_element(By.XPATH, site['nextPageSearchPattern']).get_attribute('href')
        # print("Next page link was found:", nextPageLink)
        url = nextPageLink
      except:
        if (site['countNextPage'] is True):
          currentPage += 1
          url = site['baseUrl'].rsplit('/', 1)[0] + "/" + str(currentPage)
          # print("Next page link was built:", url)
        elif (site['countNextPage'] is False):
          print("Page counter explicitly disabled")
          break
        else:
          # print("No next page found")
          break
    except:
      break

driver.quit()

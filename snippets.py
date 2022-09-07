#!/usr/bin/python3

from urllib.parse import urlparse
from pymongo import MongoClient
import logging as log
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

# instanciate logger
logger = log.getLogger('discovernewids')
logger.setLevel(log.DEBUG)
formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = log.StreamHandler()
ch.setLevel(log.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

# selenium chromium
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)



# Snippets

page = "https://www.brazzers.com/site/67/mommy-got-boobs"
nextpattern = "//ul/li[last()-1]"
videopattern = "//div[@aria-atomic = 'true']//span/a"

driver.get(page)
print(driver.find_element(By.XPATH, videopattern).get_attribute('textContent'))
driver.find_element(By.XPATH, nextpattern).click()
print(driver.find_element(By.XPATH, videopattern).get_attribute('textContent'))







# coll = db['wicked']

# while True:
#   try:
#     doc = coll.find_one({"posterlocation": {"$regex": ".*\.webp"}})
#     print(doc['_id'])
#     # doc['id'] = urlparse(doc['url']).path.rsplit('/', 1)[-1]
#     #doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
#     doc['posterlocation'] = doc['posterlocation'].replace('webp', 'jpg')
#     coll.find_one_and_update({"_id": doc['_id']}, {"$set": doc})
#   except:
#     break


# coll.update_many({}, {"$rename": {"category": "categories"}} )

# CREATE UNIQUE INDEXES

# coll.create_index( [( "url", 1 )], unique=True )
# coll.create_index( [( "id" , 1 )], unique=True, sparse=True )
# coll.create_index( [( "id" , 1 ), ("channel", 1)], unique=True, sparse=True )
# coll.create_index( [( "id_2" , 1 )], unique=True, sparse=True )
#!/usr/bin/python3

from urllib.parse import urlparse
from pymongo import MongoClient
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive
# Snippets

coll = db['vixen']

while True:
  try:
    doc = coll.find_one({"posterlocation": {"$regex": ".*\.webp"}})
    print(doc['_id'])
    # doc['id'] = urlparse(doc['url']).path.rsplit('/', 1)[-1]
    #doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    doc['posterlocation'] = doc['posterlocation'].replace('webp', 'jpg')
    coll.find_one_and_update({"_id": doc['_id']}, {"$set": doc})
  except:
    break


# coll.update_many({}, {"$rename": {"category": "categories"}} )


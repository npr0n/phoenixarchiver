from urllib.parse import urlparse
from pymongo import MongoClient
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive
# Snippets

coll = db['kink']

while True:
  try:
    doc = coll.find_one({"id": {"$exists": False}})
    print(doc['_id'])
    doc['id'] = urlparse(doc['url']).path.rsplit('/', 1)[-1]
    #doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
    coll.find_one_and_update({"_id": doc['_id']}, {"$set": doc})
  except:
    break

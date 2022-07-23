from time import sleep
from urllib.parse import urlparse
from urllib import request
import os
from pymongo import MongoClient


site = "mylf"




# directory for saved images
imagestore = "/mnt/naspool/media/porn/db-imagestore"

# db connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

collection = db[site]
print("Working on", site)
# use maximum or while True
# for number in range(updatemaxnumber):
while True:
  try:
    doc = collection.find_one({"posterlocation": {"$exists": False}, "posterurl": {"$exists": True} })
    print(doc['_id'])
  except:
    print("Did not find dataset without title.")
    break

  # poster download
  try:
    print(doc['posterurl'])
    posterfn = "/" + site + "/" + doc['id'] + os.path.splitext(urlparse(doc['posterurl']).path)[1]
    print(posterfn)
    if not os.path.exists(imagestore + posterfn):
      request.urlretrieve(doc['posterurl'], imagestore + posterfn)
      doc['posterlocation'] = posterfn
    else:
      doc['posterlocation'] = posterfn
    
    filter = { '_id': doc['_id']}
    collection.update_one(filter, { '$set': doc })

  except:
    continue

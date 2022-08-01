from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive


# KINK
collection = db['kink']
print("working on kink")
while True:
  try:
    doc = collection.find_one({"dateymd": {"$exists": False}})
    #print(doc['_id'])
  except:
    break
  
  try:
    dateymd = datetime.strptime(doc['datesite'], '%B %d, %Y').strftime('%y.%m.%d')
    filter = { '_id': doc['_id']}
    collection.update_one(filter, { '$set': {'dateymd': dateymd} })
    print("updated", doc['_id'], "with", dateymd)
  except:
    break

# VIXEN
print("working on vixen")
collection = db['vixen']
while True:
  try:
    doc = collection.find_one({"dateymd": {"$exists": False}})
    #print(doc['_id'])
  except:
    break
  
  try:
    dateymd = datetime.strptime(doc['datesite'], '%B %d, %Y').strftime('%y.%m.%d')
    filter = { '_id': doc['_id']}
    collection.update_one(filter, { '$set': {'dateymd': dateymd} })
    print("updated", doc['_id'], "with", dateymd)
  except:
    break

# MYLF
collection = db['mylf']
print("working on mylf")
while True:
  try:
    doc = collection.find_one({"dateymd": {"$exists": False}})
    #print(doc['_id'])
  except:
    break
  
  try:
    dateymd = datetime.strptime(doc['datesite'], '%m/%d/%Y').strftime('%y.%m.%d')
    filter = { '_id': doc['_id']}
    collection.update_one(filter, { '$set': {'dateymd': dateymd} })
    print("updated", doc['_id'], "with", dateymd)
  except:
    break

# DEVILSFILM
collection = db['devilsfilm']
print("working on devilsfilm")
while True:
  try:
    doc = collection.find_one({"dateymd": {"$exists": False}})
    #print(doc['_id'])
  except:
    break
  
  try:
    dateymd = datetime.strptime(doc['datesite'], '%Y-%m-%d').strftime('%y.%m.%d')
    filter = { '_id': doc['_id']}
    collection.update_one(filter, { '$set': {'dateymd': dateymd} })
    print("updated", doc['_id'], "with", dateymd)
  except:
    break


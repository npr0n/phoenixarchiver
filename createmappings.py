
from pymongo import MongoClient

client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

mappingscollection = db['mappings']

collections = [
  "adulttime",
  "bangbros",
  "brazzers",
  "brazzers_collections",
  "genderx",
  "genderx_collections",
  "kink",
  "mylf",
  "vixen",
  "wicked"
]

for site in collections:
  # print(site)
  collection = db[site]
  channels = collection.distinct("channel")
  # print(channels)
  for channel in channels:
    channel = channel.replace(' ','').lower()
    mappingscollection.update_one({"source": channel}, {"$set": {"target": site} }, upsert=True )
    print("added mapping:", channel, site)

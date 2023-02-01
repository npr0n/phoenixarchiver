from pymongo.mongo_client import MongoClient
import pymongo.errors

def init_db(uri: str, database: str):
  client = MongoClient(uri)
  db = client.get_database(database)
  return db

def upsert(collection, object, key: str):
  try:
    collection.update_one({f"{key}": object[key]}, {"$set": object}, upsert=True)
  except pymongo.errors.DuplicateKeyError:
    # this is most likely due to a race condition because of upsert and multiple keys
    return 0

def find_one_no_title(collection):
  try:
    doc = collection.find_one({"title": {"$exists": False}})
    return doc
  except:
    print("Did not find dataset without title")
    return 1
#!/usr/bin/python3

from variables import *
from pymongo.mongo_client import MongoClient
import pymongo.errors

def init_db(uri: str, database: str):
  client = MongoClient(uri)
  db = client.get_database(database)
  return db

def init_default_db(uri = MONGODB_URI, database = MONGODB_DATABASE):
  db = init_db(uri = uri, database = database)
  return db

def upsert(collection, doc, key: str):
  try:
    collection.update_one({f"{key}": doc[key]}, {"$set": doc}, upsert=True)
  except pymongo.errors.DuplicateKeyError:
    # this is most likely due to a race condition because of upsert and multiple keys
    return 0

def find_one_and_delete(collection, doc, key: str):
  try:
    collection.find_one_and_delete({f"{key}": doc[key]})
  except:
    print("could not delete doc from db:", doc)

def find_one_no_title(collection):
  try:
    doc = collection.find_one({"title": {"$exists": False}})
    return doc
  except:
    print("Did not find dataset without title")
    return 1
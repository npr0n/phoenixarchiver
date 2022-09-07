#!/usr/bin/python3

from time import sleep
from urllib.parse import urlparse
import urllib
import os
from pymongo import MongoClient
from PIL import Image


sites = [
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

retry_errors = False

maxattempts = 5

# directory for saved images
imagestore = "/mnt/naspool/media/porn/db-imagestore"

# db connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive

# headers
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', user_agent)]
urllib.request.install_opener(opener)

for site in sites:
  collection = db[site]
  print("Working on", site)

  # reset all posterlocations with 404 error placeholder
  if retry_errors is True:
    collection.update_many({"posterlocation": "404"}, {"$unset": {"posterlocation": " "}})

  while True:
    
    convert_to_jpg = False

    try:
      doc = collection.find_one({"posterlocation": {"$exists": False}, "posterurl": {"$exists": True} })
      print(doc['_id'])
    except:
      # print("Did not find dataset without posterlocation.")
      break

    # poster download
    try:
      # print(doc['posterurl'])
      posterfn = "/" + site + "/" + doc['id'] + os.path.splitext(urlparse(doc['posterurl']).path)[1]

      # prepare conversion to jpg
      if os.path.splitext(posterfn)[1] == ".webp":
        posterfn = os.path.splitext(posterfn)[0] + ".jpg"
        convert_to_jpg = True

      # print(posterfn)
      if doc['id'] is None:
        print("database entry does not contain movie id! :", doc['_id'])
      
      posterfile = imagestore + posterfn
      # print(posterfile)
      if not os.path.exists(posterfile):
        # print("poster does not exist")
        for attempt in range(maxattempts):
          # print("(" + attempt + "/" + maxattempts + ")")
          try:
            response = urllib.request.urlopen(doc['posterurl'])
            content = response.read()

            if convert_to_jpg:
              Image.open(content).convert("RGB").save(posterfile, "jpeg")
            else:
              out_file = open(posterfile, "wb")
              out_file.write(content)
            
            doc['posterlocation'] = posterfn
            break
          except:
            print("Could not download poster:", doc['posterurl'])
            doc['posterlocation'] = "404"
            print(site, doc['id'])
            sleep(1)
          break
      else:
        print("poster exists already")
        doc['posterlocation'] = posterfn
      
      filter = { '_id': doc['_id']}
      collection.update_one(filter, { '$set': doc })

    except:
      sleep(1)
      continue

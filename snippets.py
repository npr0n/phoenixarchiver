# Snippets

coll = db['devilsfilm']

while True:
   try:
     doc = coll.find_one({"id_2": {"$exists": False}})
     doc['id_2'] = urlparse(doc['url']).path.rsplit('/', 2)[-2]
     coll.find_one_and_update({"_id": doc['_id']}, {"$set": doc})
   except:
     break

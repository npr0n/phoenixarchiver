from pymongo import MongoClient

client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive
mappings = db['mappings']

kinksources = "30minutesoftorment boundgangbangs boundgods boundinpublic brutalsessions buttmachineboys devicebondage divinebitches electrosluts \
everythingbutt familiestied filthyfemdom footworship fuckingmachines gangbang gaybondage gayfetish hardcoregangbang hogtied kink kinkclassics \
kinkfeatures kinkmenclassics kinkuniversity kinkybites meninpain menonedge nakedkombat publicdisgrace sadisticrope sexandsubmission thetrainingofo \
theupperfloor tspussyhunters tsseduction ultimatesurrender waterbondage whippedass wiredpussy"

mylfsources = "mylfofthemonth mylfwood shoplyftermylf sofiemariexxx gotmylf mylf mylfblows mylflabs mylfselects mylfxmandyflores mylfxmisslexa newmylfs"


kinkarray = kinksources.split()
for source in kinkarray:
  try:
    mappings.insert_one({"source": source, "target": "kink"})
  except:
    pass

mylfarray = mylfsources.split()
for source in mylfarray:
  try:
    mappings.insert_one({"source": source, "target": "mylf"})
  except:
    pass



#mappings.insert_one({"source": "deeper", "target": "deeper"})
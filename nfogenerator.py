from pymongo import MongoClient
import sys
import os
from lxml import etree as ET
from lxml.etree import CDATA
from datetime import datetime
import json
import glob
import requests

# mongodb connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive
mappings = db['mappings']

# directory
basedir = "/mnt/naspool/media/porn/movies"

nfotestfile = "/mnt/naspool/nas/scripts/phoenixarchiver/testfile.nfo"

### read from existing nfo file

nfofiles = []
for root, dirs, files in os.walk(basedir):
  for file in files:
      if file.endswith(".nfo"):
        nfofiles.append(os.path.join(root, file))
#print(nfofiles)

# find and parse the nfo files (xml)
for nfofile in nfofiles:
  filename = os.path.basename(nfofile)
  tree = ET.parse(nfofile)
  root = tree.getroot()
  nfotitle = root.find('title').text

  ### if lockdata is true we assume this script already ran
  try:
    if (root.find('lockdata').text == "true"):
      #print("nfofile has locked data. skipping...")
      continue
  except:
    pass

  if filename.rsplit('.', 1)[0].lower() == nfotitle.lower():
    #print(nfotitle)

    try:
      ### get title and build search query
      nfochannel = nfotitle.split('.')[0].lower()
      date = None
      movieid = None
      actor = None

      # map channel to database
      try:
        channel = mappings.find_one({"source": nfochannel})["target"]
        #print("mapped", nfochannel, "to", channel)
      except:
        #print("could not map", nfochannel, "to any database:", nfotitle)
        continue

      # try to extract a valid date or id
      try:
        date = '.'.join(map(str, nfotitle.split('.')[1:4]))
        dateformatted = datetime.strptime(date, '%y.%m.%d').strftime('%Y-%m-%d')
      except:
        #print("no valid date found in filename:", nfotitle)
        date = None
        pass

      # try matching via id
      if (date is None):
        try:
          movieid = nfotitle.split('.')[1]
          #print("trying to match via id:", movieid, nfotitle)
        except:
          print("could not extract id:", nfotitle)
          continue
      
      if (movieid is None):
        try:
          actor = nfotitle.split('.')[4]
          #print("actor:", actor)
        except:
          print("no valid actor name found in filename:", nfotitle)
          continue

      # get document from database
      try:
        #print(channel, date, actor)
        if (date is not None):
          doc = db[channel].find_one({"dateymd": date, "actors": {"$regex": actor, "$options": "i"}})
          if (doc is None):
            #print("got empty doc from database:", nfotitle)
            try:
              doc = db[channel].find_one({"dateymd": date, "channel": {"$regex": nfochannel[:2]}})
              #print(doc, nfochannel)
              print("found something matching the date. please check manually!", doc['title'], nfotitle)
            except:
              continue
        elif (movieid is not None):
          doc = db[channel].find_one({"url": {"$regex": movieid, "$options": "i"}})
          if (doc is None):
            #print("got empty doc from database:", nfotitle)
            continue
      except:
        print("could not match to date and actor first name:", nfotitle)
        continue

      # update tree from doc
      try:
        #print("updating xml")
        title = root.find('title')
        title.text = doc['title']

        try:
          root.find('sorttitle').text = doc['title']
        except:
          try:
            sorttitle = ET.Element('sorttitle')
            sorttitle.text = doc['title']
            title.addnext(sorttitle)
          except:
            print("could not insert sorttitle element:", nfotitle)
            continue

        try:
          root.find('plot').text = CDATA(doc['description'])
        except:
          try:
            plot = ET.Element('plot')
            plot.text = CDATA(doc['description'])
            title.addnext(plot)
          except:
            print("could not insert plot element:", nfotitle)
            continue
        
        mpaa = ET.Element('mpaa')
        mpaa.text = "XXX"

        try:
          settitle = doc['collectiontitle']
          setelem = ET.Element('set')
          setname = ET.SubElement(setelem, 'name')
          setname.text = settitle
          root.append(setelem)
        except:
          pass

        studio = ET.Element('studio')
        studio.text = channel.capitalize()
        root.append(studio)

        # if channel was mapped from filename / title add original as well as mapped
        if channel != nfochannel:
          studio2 = ET.Element('studio')
          studio2.text = nfochannel.capitalize()
          root.append(studio2)
        
        premiered = ET.Element('premiered')
        releasedate = ET.Element('releasedate')
        premiered.text = releasedate.text = dateformatted

        title.addnext(premiered)
        title.addnext(releasedate)
        title.addnext(mpaa)

      except:
        print("update part 1 did not work:", nfotitle)


      # update tree with actors
      try:
        for actor in doc['actors']:
          elem = ET.Element('actor')
          name = ET.SubElement(elem, 'name')
          name.text = actor
          actype = ET.SubElement(elem, 'type')
          actype.text = 'Actor'
          title.addnext(elem)
      except:
        print("updating actors did not work")


      # update tree with collection
      try:
        for category in doc['collection']:
          elem = ET.Element('genre')
          elem.text = category
          root.append(elem)
      except:
        print("updating categories did not work")


      # write tree to file
      try:
        try:
          lockdata = root.find('lockdata')
          lockdata.text = "true"
        except:
          lockdata = ET.Element('lockdata')
          lockdata.text = "true"
          root.append(lockdata)

        ET.indent(tree, '  ')
        tree.write(nfofile, pretty_print=True, xml_declaration=True, encoding='utf-8')
      except:
        print("writing to file did not work")
        sys.exit(0)
      

      ### if not exists try getting the poster
      try:
        dirname = os.path.dirname(nfofile)
        if glob.glob(dirname + "/poster*"):
          print("poster already exists")
        else:
          #print("no poster found in", dirname)
          if doc['posterurl']:
            #print("getting poster from", doc['posterurl'])
            filelocation = dirname + "/poster." + doc['posterurl'].split('?')[0].rsplit('.', 1)[1]
            r = requests.get(doc['posterurl'])
            #print("writing file")
            open(filelocation, 'wb').write(r.content)
      except:
        print("detecting or downloading poster failed")


      # try:
      #   print("old:", nfotitle)
      #   print("new:", doc['title'])
      # except:
      #   pass
      #sys.exit(0)
    except:
      continue
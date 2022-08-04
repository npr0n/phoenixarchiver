#!/usr/bin/python3

from pymongo import MongoClient
import sys
import os
from lxml import etree as ET
from lxml.etree import CDATA
from datetime import datetime
import glob
import requests
import shutil

# mongodb connection
client = MongoClient("mongodb://phoenixinserter:phoenix@localhost:27017/phoenixarchive")
db = client.phoenixarchive
mappings = db['mappings']

# directory
basedir = "/mnt/naspool/media/porn"
importdir = basedir + "/manualimport"
targetdir = basedir + "/movies"
dbimagestore = basedir + "/db-imagestore"


# find and parse the movie files
#while True:

for rootdir, subdirs, files in os.walk(importdir):
  for moviefile in files:
    # file base name
    filename = os.path.basename(moviefile)
    
    # clear doc variable
    try:
      del doc
    except:
      pass
    
    if os.path.splitext(moviefile)[1] in [".mkv", ".mp4"]:
      #print("movie filename:", os.path.join(rootdir, moviefile))
      
      #print("found movie:", moviefile)
      nfofile = os.path.splitext(moviefile)[0] + ".nfo"
      #print("nfofile:", nfofile)
      
      if os.path.exists(nfofile):
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

      else:
        root = ET.Element("movie")
        tree = ET.ElementTree(root)
        nfotitle = os.path.splitext(moviefile)[0]


      #################################################
      ### identify movie

      nfochannel = nfotitle.split('.')[0].lower()
      date = None
      movieid = None
      actor = None

      # map channel to database
      try:
        channel = mappings.find_one({"source": nfochannel})["target"]
        #print("mapped", nfochannel, "to", channel)
      except:
        print("could not map", nfochannel, "to any database:", nfotitle)
        continue

        # try to extract a valid date or id
      try:
        date = '.'.join(map(str, nfotitle.split('.')[1:4]))
        dateformatted = datetime.strptime(date, '%y.%m.%d').strftime('%Y-%m-%d')
      except:
        #print("no valid date found in filename:", nfotitle)
        date = None
        pass
      try:
        actor = nfotitle.split('.')[4]
        #print("actor:", actor)
      except:
        # print("no valid actor name found in filename:", nfotitle)
        continue

      # try matching via id
      if (date is None):
        try:
          movieid = nfotitle.split('.', 1)[1].rsplit('.', 1)[0].split('.xxx')[0].replace('.', ' ')
          # print("trying to match via id:", movieid, nfotitle)

          #moviename = nfotitle.split('.', 1)[1].rsplit('.', 1)[0].split('.xxx')[0].replace('.', ' ')

        except:
          print("could not extract id:", nfotitle)
          continue
      

###########################################################
      # get document from database
      try:
        #print(channel, date, actor)
        if (date is not None):
          doc = db[channel].find_one({"dateymd": date, "actors": {"$regex": actor, "$options": "i"}})
          if (doc is None):
            # print("got empty doc from database:", nfotitle)
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

      print("Found match:", doc['title'])
      print("Database ID:", doc['_id'])

#########################################################
      # build or modify the nfo
      
      try:
        title = root.find('title')
        title.text = doc['title']
      except:
        title = ET.Element('title')
        title.text = doc['title']
        root.append(title)
      
      try:
        root.find('sorttitle').text = doc['title']
      except:
        try:
          sorttitle = ET.Element('sorttitle')
          sorttitle.text = doc['title']
          title.addnext(sorttitle)
        except:
          print("could not insert sorttitle element:", nfotitle)
          pass

      try:
        root.find('plot').text = CDATA(doc['description'])
      except:
        try:
          plot = ET.Element('plot')
          plot.text = CDATA(doc['description'])
          title.addnext(plot)
        except:
          #print("could not insert plot element:", nfotitle)
          pass
      
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


      # update tree with category
      try:
        for category in doc['categories']:
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
        nfolocation = os.path.join(rootdir, nfofile)
        #print(nfolocation)
        tree.write(nfolocation, pretty_print=True, xml_declaration=True, encoding='utf-8')
      except:
        print("writing nfo to file did not work")
        sys.exit(69)


##########################################################
      ### if not exists try getting the poster
      try:
        #print(rootdir)
        if not glob.glob(rootdir + "/" + os.path.splitext(nfofile)[0] + "-poster.*"):
          #print("no poster found in", rootdir)

          if doc['posterlocation']:
            sourcefile = dbimagestore + doc['posterlocation']

            if os.path.exists(sourcefile):
              targetfile = rootdir + "/" + os.path.splitext(nfofile)[0] + "-poster" + os.path.splitext(sourcefile)[1]
              #print(targetfile)
              shutil.copyfile(sourcefile, targetfile)
            else:
              print("location from database does not exist!", sourcefile)

          elif doc['posterurl']:
            print("getting poster from", doc['posterurl'])
            filelocation = rootdir + "/" + os.path.splitext(nfofile)[0] + "-poster." + doc['posterurl'].split('?')[0].rsplit('.', 1)[1]
            r = requests.get(doc['posterurl'])
            print("writing file")
            open(filelocation, 'wb').write(r.content)
          else:
            print("could not get poster from database info")
        else:
          pass
      except:
        #print("detecting or downloading poster failed")
        pass


#########################################################
      # create new folder name
      try:
        removethese = [":",";","/","\\","'",'"']
        underscorethese = [".", " ", "!","?",'$']
        newfoldername = doc['title']
        for i in underscorethese:
          newfoldername = newfoldername.replace(i, '_')
        for i in removethese:
          newfoldername = newfoldername.replace(i, '')
        newfoldername = newfoldername + "_-_" + datetime.strptime(doc['dateymd'], '%y.%m.%d').strftime('%Y')
        target = targetdir + "/" + newfoldername
        print("Old Folder :", rootdir)
        print("New Folder :      ", target)

        # handle folder already exists; usually duplicate movie
        if os.path.exists(target):
          print("New Folder already exists. Probably a duplicate, moving anyway")
        shutil.move(rootdir, target)
      except:
        pass


      

####################################################################

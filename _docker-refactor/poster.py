#!/usr/bin/python3

import os
import subprocess
from variables import *
import dbase
import wdriver
import requests
from PIL import Image

def mega_login(username: str, password: str):
  try:
    if VERBOSE:
      subprocess.run(["mega-login", username, password])
    else:
      subprocess.run(["mega-login", username, password], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  except:
    print("mega login failed")

def mega_logout():
  if VERBOSE:
    subprocess.run("mega-logout", stdout=subprocess.DEVNULL)
  else:
    subprocess.run("mega-logout", stdout=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def mega_upload_file(source: os.PathLike, target: str):
  if VERBOSE:
    subprocess.run(["mega-put", "-c", source, target])
  else:
    subprocess.run(["mega-put", "-c", source, target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def mega_get_sharelink(file: str):
  if VERBOSE:
    print(f"file: {file}")
  megaurl = subprocess.run(["mega-export", "-f", "-a", file], capture_output=True, text=True).stdout.split(f"{file}:")[1].strip()
  if VERBOSE:
    print(f"megaurl: {megaurl}")
  return megaurl

def mega_signup(username: str, password: str, friendlyname: str):
  subprocess.run(["mega-signup", username, password, f'--name="{friendlyname}"'])

def download_from_url(url: str, targetfile: str = "/tmp/poster.png"):
  # correct potential file extension mismatch
  ext = os.path.splitext(url)[1]
  targetfile = targetfile.rsplit(".")[0] + ext

  # download and write to file
  with open(targetfile, "wb") as f:
    f.write(requests.get(url).content)

  # if extension is webp convert to png
  if ext == ".webp":
    if VERBOSE:
      print("converting .webp to .png")
    targetfile = convert_imageformat(file=targetfile)

  # return targetfile in case of extension correction
  return targetfile

def convert_imageformat(file: str, targetformat: str = "png"):
  newfile = file.rsplit(".")[0] + "." + targetformat
  im = Image.open(file).convert("RGB")
  im.save(newfile, targetformat)
  return newfile

def upload_and_share(sourcefile: os.PathLike, id: str):
  targetfile = id + os.path.splitext(sourcefile)[1]
  mega_upload_file(source=sourcefile, target=targetfile)
  if VERBOSE:
    print(f"uploaded file {targetfile}")
  sharelink = mega_get_sharelink(targetfile)
  return sharelink


def poster_download_from_doc(doc, targetfile: str = "/tmp/poster.png"):
  posterurl = doc['posterurl']
  if VERBOSE:
    print(f"posterurl: {posterurl}")
  # targetfile will get the extension corrected
  targetfile = download_from_url(url=posterurl)
  if VERBOSE:
    print(f"targetfile: {targetfile}")

  # file gets uploaded, shared and the link returned to be entered into doc
  if VERBOSE:
    print(f"id: {doc['id']}")

  doc['postermegalink'] = upload_and_share(sourcefile=targetfile, id=doc['id'])
  
  # remove file from disk
  delete_file(targetfile)

  return doc

def delete_file(file):
  if os.path.exists(file):
    os.remove(file)

def collection_poster_downloader(collection):
  while True:
    try:
      doc = dbase.find_one_no_mega(collection)
      if VERBOSE:
        print(f"found doc: {doc}")
    except:
      if VERBOSE:
        print("did not find doc without mega link")
      False
    
    doc = poster_download_from_doc(doc)
    dbase.upsert(collection=collection, doc=doc, key="_id")
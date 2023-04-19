#!/usr/bin/python3

import adulttime
import bangbros
import brazzers
import genderx
import kink
import mylf
import vixen
import wicked
from variables import VERBOSE
from variables import *

def discoverSites():
  if VERBOSE:
    print("#######################")
    print("# BEGINNING DISCOVERY #")
    print("#######################")
  
  try:
    adulttime.discovery(VERBOSE)
  except:
    print("failed adulttime discovery")
  
  try:
    bangbros.discovery(VERBOSE)
  except:
    print("failed bangbros discovery")
  
  try:
    brazzers.discovery(VERBOSE)
  except:
    print("failed brazzers discovery")
  
  try:
    genderx.discovery(VERBOSE)
  except:
    print("failed genderx discovery")
  
  try:
    kink.discovery(VERBOSE)
  except:
    print("failed kink discovery")
  
  try:
    mylf.discovery(VERBOSE)
  except:
    print("failed mylf discovery")
  
  try:
    vixen.discovery(VERBOSE)
  except:
    print("failed vixen discovery")
  
  try:
    wicked.discovery(VERBOSE)
  except:
    print("failed wicked discovery")
  
  if VERBOSE:
    print("######################")
    print("# FINISHED DISCOVERY #")
    print("######################")
  


def scrapeSites():
  if VERBOSE:
    print("######################")
    print("# BEGINNING SCRAPERS #")
    print("######################")
  
  try:
    adulttime.scraper(VERBOSE)
  except:
    print("failed adulttime scraper")
  
  try:
    bangbros.scraper(VERBOSE)
  except:
    print("failed bangbros scraper")
  
  try:
    brazzers.scraper(VERBOSE)
  except:
    print("failed brazzers scraper")
  
  try:
    genderx.scraper(VERBOSE)
  except:
    print("failed genderx scraper")
  
  try:
    kink.scraper(VERBOSE)
  except:
    print("failed kink scraper")
  
  try:
    mylf.scraper(VERBOSE)
  except:
    print("failed mylf scraper")
  
  try:
    vixen.scraper(VERBOSE)
  except:
    print("failed vixen scraper")
  
  try:
    wicked.scraper(VERBOSE)
  except:
    print("failed wicked scraper")
  
  if VERBOSE:
    print("#####################")
    print("# FINISHED SCRAPERS #")
    print("#####################")
  


def downloadPosters():
  if VERBOSE:
    print("################################")
    print("# BEGINNING POSTER DOWNLOADERS #")
    print("################################")
  
  try:
    adulttime.poster_downloader(VERBOSE)
  except:
    print("failed adulttime poster_downloader")
  
  # try:
  #   bangbros.poster_downloader(VERBOSE)
  # except:
  #   print("failed bangbros poster_downloader")
  
  # try:
  #   brazzers.poster_downloader(VERBOSE)
  # except:
  #   print("failed brazzers poster_downloader")
  
  # try:
  #   genderx.poster_downloader(VERBOSE)
  # except:
  #   print("failed genderx poster_downloader")
  
  try:
    kink.poster_downloader(VERBOSE)
  except:
    print("failed kink poster_downloader")
  
  # try:
  #   mylf.poster_downloader(VERBOSE)
  # except:
  #   print("failed mylf poster_downloader")
  
  # try:
  #   vixen.poster_downloader(VERBOSE)
  # except:
  #   print("failed vixen poster_downloader")
  
  # try:
  #   wicked.poster_downloader(VERBOSE)
  # except:
  #   print("failed wicked poster_downloader")
  
  if VERBOSE:
    print("###############################")
    print("# FINISHED POSTER DOWNLOADERS #")
    print("###############################")
  


if __name__ == "__main__":
  print(f"MONGODB_URI: {MONGODB_URI}")
  discoverSites()
  scrapeSites()
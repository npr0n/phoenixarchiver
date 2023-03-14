#!/usr/bin/python3

import adulttime
import bangbros
import brazzers
import genderx
import kink
import mylf
import vixen
import wicked

def discoverSites():
  try:
    adulttime.discovery()
  except:
    print("failed adulttime discovery")
  
  try:
    bangbros.discovery()
  except:
    print("failed bangbros discovery")
  
  try:
    brazzers.discovery()
  except:
    print("failed brazzers discovery")
  
  try:
    genderx.discovery()
  except:
    print("failed genderx discovery")
  
  try:
    kink.discovery()
  except:
    print("failed kink discovery")
  
  try:
    mylf.discovery()
  except:
    print("failed mylf discovery")
  
  try:
    vixen.discovery()
  except:
    print("failed vixen discovery")
  
  try:
    wicked.discovery()
  except:
    print("failed wicked discovery")


def scrapeSites(verbose: bool = False):
  try:
    adulttime.scraper(verbose=verbose)
  except:
    print("failed adulttime scraper")
  
  try:
    bangbros.scraper(verbose=verbose)
  except:
    print("failed bangbros scraper")
  
  try:
    brazzers.scraper(verbose=verbose)
  except:
    print("failed brazzers scraper")
  
  try:
    genderx.scraper(verbose=verbose)
  except:
    print("failed genderx scraper")
  
  try:
    kink.scraper(verbose=verbose)
  except:
    print("failed kink scraper")
  
  try:
    mylf.scraper(verbose=verbose)
  except:
    print("failed mylf scraper")
  
  try:
    vixen.scraper(verbose=verbose)
  except:
    print("failed vixen scraper")
  
  try:
    wicked.scraper(verbose=verbose)
  except:
    print("failed wicked scraper")


if __name__ == "__main__":
  discoverSites()
  scrapeSites()
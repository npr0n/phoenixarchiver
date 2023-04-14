#!/usr/bin/python3

import adulttime
import bangbros
import brazzers
import genderx
import kink
import mylf
import vixen
import wicked
import variables

def discoverSites(verbose: bool = False):
  try:
    adulttime.discovery(verbose=verbose)
  except:
    print("failed adulttime discovery")
  
  try:
    bangbros.discovery(verbose=verbose)
  except:
    print("failed bangbros discovery")
  
  try:
    brazzers.discovery(verbose=verbose)
  except:
    print("failed brazzers discovery")
  
  try:
    genderx.discovery(verbose=verbose)
  except:
    print("failed genderx discovery")
  
  try:
    kink.discovery(verbose=verbose)
  except:
    print("failed kink discovery")
  
  try:
    mylf.discovery(verbose=verbose)
  except:
    print("failed mylf discovery")
  
  try:
    vixen.discovery(verbose=verbose)
  except:
    print("failed vixen discovery")
  
  try:
    wicked.discovery(verbose=verbose)
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
  discoverSites(verbose=variables.VERBOSE)
  scrapeSites(verbose=variables.VERBOSE)
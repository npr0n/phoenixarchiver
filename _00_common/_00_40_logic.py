from ._00_10_common import *
from ._00_20_driver import *
from ._00_30_db import *

def loop_through_sites(db, driver, sites: list, maxPage: int = 1, initPage: int = 1):
  for site in sites:
    discover_site(db, driver, site, maxPage, initPage)

def discover_site(db, driver, site: dict, maxPage: int = 1, initPage: int = 1):
  
  print("working on site:", site['baseUrl'])
  try:
    driver.get(site['baseUrl'])
  except:
    print("could not get page", site['baseUrl'])
  
  try:
    parse_search_pages(driver, site, db[site['collection']], maxPage, initPage)
  except:
    print("something went wrong in parse_search_pages")
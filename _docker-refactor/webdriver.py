#!/usr/bin/python3

from variables import *
from database import *
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.parse import urlparse
from time import sleep

def get_useragent(driver):
  useragent = driver.execute_script("return navigator.userAgent")
  return useragent

def init_driver(command_executor: str, useragent: str = "", driver_iwait: int = 10, headless: bool = True, printoptions: bool = False):
  
  options = wd.ChromeOptions()
  if headless:
    options.headless = True
    options.add_argument('disable-gpu')
    options.add_argument("window-size=1024,768")
  if useragent != "":
    options.add_argument(f'user-agent={useragent}')
  
  if printoptions:
    print(options.arguments)
  
  driver = wd.Remote(command_executor = command_executor, options = options)
  driver.implicitly_wait(driver_iwait)
  
  return(driver)

def init_default_driver(command_executor = SELENIUM_URI, useragent = SELENIUM_USERAGENT, driver_iwait = 30, headless = SELENIUM_HEADLESS, printoptions: bool = False):
  driver = init_driver(command_executor = command_executor, useragent = useragent, driver_iwait = driver_iwait, headless = headless, printoptions = printoptions)
  return driver

def parse_element(elem, site):
  result = {}
  result['url'] = elem.get_attribute('href')
  result['id'] = urlparse(result['url']).path.rpartition('/')[-1]
  try:
    if site['channel']:
      result['channel'] = site['channel']
    else:
      if site['channelSearchPattern']:
        result['channel'] = elem.find_element(By.XPATH, site['channelSearchPattern']).get_attribute('textContent').lower().replace(' ','').replace(',','').replace("'",'').replace('!','').replace('?','')
  except:
    pass
  
  try:
    if site['ratingSearchPattern']:
      result['rating'] = elem.find_element(By.XPATH, site['ratingSearchPattern']).get_attribute('textContent')
  except:
    pass
  
  try:
    if site['dateSearchPattern']:
      result['datesite'] = elem.find_element(By.XPATH, site['dateSearchPattern']).get_attribute('textContent')
  except:
    pass

  return result

def navigate_to_next_page(driver, pattern: str, method: str = "XPATH"):
  if method == "LINK_TEXT":
    nextPageElement = driver.find_element(By.LINK_TEXT, pattern)
  elif method == "ID":
    nextPageElement = driver.find_element(By.ID, pattern)
  else:
    nextPageElement = driver.find_element(By.XPATH, pattern)

  actions = ActionChains(driver)
  actions.scroll_to_element(nextPageElement)
  actions.perform()

  try:
    nextPageElement.click()
  except:
    actions = ActionChains(driver)
    actions.scroll_by_amount(0, 150)
    actions.perform()
    sleep(1)
    nextPageElement.click()

def parse_search_pages(driver, site: dict, collection, maxPage: int = 1, pageCounter: int = 1):
  while pageCounter <= maxPage:
    
    try:
      elems = driver.find_elements(By.XPATH, site['resultSearchPattern'])

      for elem in elems:
        result = parse_element(elem, site)
        upsert(collection, result, 'url')

    except NoSuchElementException:
      print("no such element exception")
      break

    try:
      navigate_to_next_page(driver, site["nextPageSearchPattern"], site["method"])
      pageCounter += 1
    except:
      print("could not navigate further")
      return 0
  
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

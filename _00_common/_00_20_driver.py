from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.parse import urlparse
from ._00_30_db import upsert
from time import sleep

def init_driver(useragent: str, command_executor: str, driver_iwait: int = 10, headless: bool = True):
  
  options = webdriver.ChromeOptions()
  if headless:
    options.headless = True
    options.add_argument('disable-gpu')
    options.add_argument("window-size=1024,768")
  options.add_argument(f'useragent={useragent}')

  driver = webdriver.Remote(command_executor = command_executor, options = options)
  driver.implicitly_wait(driver_iwait)

  return(driver)

def parse_element(driver, elem, collection, channel = None, channelSearchPattern = None, ratingSearchPattern = None, dateSearchPattern = None):
  result = {}
  result['url'] = elem.get_attribute('href')
  result['id'] = urlparse(result['url']).path.rpartition('/')[-1]
  try:
    if channel:
      result['channel'] = channel
    else: 
      result['channel'] = elem.find_element(By.XPATH, channelSearchPattern).get_attribute('textContent').lower().replace(' ','').replace(',','').replace("'",'').replace('!','').replace('?','')
  except:
    pass
  
  try:
    result['rating'] = elem.find_element(By.XPATH, ratingSearchPattern).get_attribute('textContent')
  except:
    pass
  
  try:
    result['datesite'] = elem.find_element(By.XPATH, dateSearchPattern).get_attribute('textContent')
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
        result = parse_element(driver, elem, site["collection"])
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
  

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas
import time


service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert  "No results found." not in driver.page_source
time.sleep(6)
driver.close()
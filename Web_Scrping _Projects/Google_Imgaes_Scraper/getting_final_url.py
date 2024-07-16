from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup




service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

with open("urls.txt") as f:
    for line in f.readlines():
        if line != "\n":
            driver.get(line)
            time.sleep(8)
            print(driver.current_url)
            html=driver.find_element(By.CLASS_NAME,"")
            print(html.get_attribute('outerHTML'))
            print("\n\n\n\n")

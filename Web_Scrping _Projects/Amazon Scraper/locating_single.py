from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
query="laptop"
driver.get(f"https://www.amazon.in/s?k={query}&crid=V4MX297CAMU7&sprefix=lap%2Caps%2C246&ref=nb_sb_ss_pltr-xclick_2_3")

elem=driver.find_element(By.CLASS_NAME,"puis-card-container")
print(elem.get_attribute("outerHTML"))
time.sleep(6)
driver.close()
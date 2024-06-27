from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
query="laptop"
for i in range(1,20):
    driver.get(f"https://www.amazon.in/s?k={query}&page={i}&crid=V4MX297CAMU7&sprefix=lap%2Caps%2C246&ref=nb_sb_ss_pltr-xclick_2_3")

    elems=driver.find_elements(By.CLASS_NAME,"puis-card-container")
    print(f"{len(elems)} items found")
    for elem in elems:
        print(elem.text)
        print("\n")
        print("\n")




    # print(elem.get_attribute("outerHTML"))
    # print(elem.text)
driver.close()

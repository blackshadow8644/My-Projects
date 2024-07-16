from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.keys import Keys
import os

service=Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

driver.get("https://www.google.com/search?sca_esv=d8fb14231ead3ded&sxsrf=ADLYWIIvGw15pPnOlkdIaTh7rmkaMQfQQw:1720083931707&q=dragon&udm=2&fbs=AEQNm0Aa4sjWe7Rqy32pFwRj0UkWd8nbOJfsBGGB5IQQO6L3JzEq8sk6FPCPzvp42tv1tXrkTLHakbUui6kohY8mGbK-gBWBZuenhxh_XZeQIB0WzY43WoGFroT0AluXUlL3qT0d2WG7sWwOdlcmSxcOEQrogtDUBs9GJUwShjseUzZCqStSHxazvHGl7iiDvvnc0ed4mKZK&sa=X&ved=2ahUKEwiRv-79g42HAxXa1AIHHSD-EvMQtKgLegQIHRAB&biw=1280&bih=593")

images=driver.find_elements(By.CLASS_NAME,"H8Rx8c")
for image in images:
    try:    
        image.click()
        time.sleep(0.5)
        with open("urls.txt", "a") as f:
            if driver.current_url.endswith("mosaic"):
                f.write(f"{driver.current_url}\n\n\n")
    except:
        continue
time.sleep(5)

driver.quit()
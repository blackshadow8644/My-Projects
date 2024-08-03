from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time

# Initialize the WebDriver (make sure to have the appropriate WebDriver for your browser in your PATH)
driver = webdriver.Chrome()

# Initialize the data dictionary
d = {"category": [], "title": [], "price": [], "link": []}

# Open the main page
driver.get("https://www.thegiftshop.pk/")
driver.maximize_window()
time.sleep(5)  # Wait for the page to load

# Find all category links
links = driver.find_elements(By.CLASS_NAME, "woodmart-nav-link")

for link in links:
    try:
        final_link = link.get_attribute("href")
        if final_link and final_link.startswith("https://www.thegiftshop.pk/product"):
            driver.get(final_link)
            time.sleep(5)  # Wait for the product page to load
            
            # Extract category
            category_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            category = category_tag.text if category_tag else "No Category"
            
            # Extract titles and links
            titles_tags = driver.find_elements(By.CLASS_NAME, "wd-entities-title")
            for title_tag in titles_tags:
                title = title_tag.text.strip()
                product_link = title_tag.get_attribute("href")
                
                # Append to data dictionary
                d["category"].append(category)
                d["title"].append(title)
                d["link"].append(product_link)
                d["price"].append("No Price")  # Assuming you will handle price extraction separately

    except StaleElementReferenceException:
        print("Encountered StaleElementReferenceException, retrying...")
        continue  # Skip to the next link
    except TimeoutException:
        print("TimeoutException: Unable to find element, skipping...")
        continue  # Skip to the next link

# Close the WebDriver
driver.quit()

# Create DataFrame and save to CSV
df = pd.DataFrame(data=d)
df.to_csv("data.csv", index=False)

print("Data has been saved to data.csv")

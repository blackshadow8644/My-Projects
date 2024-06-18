import requests
from bs4 import BeautifulSoup
import pandas as pd
data={"title":[],"price":[]}


r=requests.get("https://www.hkarimbuksh.com/collections/groceries")
soup=BeautifulSoup(r.text)
tiles=soup.find_all(class_="product-item__title text--strong link")
for tile in tiles:
    print(tile.text)
    data["title"].append(tile.text)
prices=soup.find_all(class_="price")
for price in prices:
    print(price.text)
    data["price"].append(price.text)
    if len(data["price"]) == len(data["title"]):
        break
    
df=pd.DataFrame.from_dict(data)
df.to_csv("data.csv",index=False)
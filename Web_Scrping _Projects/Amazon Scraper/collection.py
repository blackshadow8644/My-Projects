from bs4 import BeautifulSoup
import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Initialize the dictionary to store data
d = {'title': [], 'price': [], 'link': [], 'MRP': [], 'Free Delivery': [], 'Star': [], 'Rating': []}

# Loop through the HTML files in the data directory
for file in os.listdir("data"):
    try:
        with open(f"data/{file}", encoding="utf-8") as f:
            html_doc = f.read()

        soup = BeautifulSoup(html_doc, "html.parser")

        # Extract the title
        t = soup.find("h2")
        title = t.get_text() if t else "None"

        # Extract the link
        l = t.find("a") if t else None
        link = f"https://amazon.in/{l['href']}" if l and l.get('href') else "None"

        # Extract the price
        p = soup.find("span", attrs={"class": "a-price-whole"})
        price = p.get_text() if p else "None"

        # Extract the MRP
        mrp = soup.find("span", attrs={"class": "a-offscreen"})
        mrp = mrp.get_text() if mrp else "None"

        # Extract the Free Delivery information
        free_delivery = soup.find("span", attrs={"class": "a-color-base"})
        free_delivery = free_delivery.get_text() if free_delivery else "None"

        # Extract the Star rating
        star = soup.find("i", attrs={"class": "a-icon a-icon-star-small a-star-small-4-5 aok-align-bottom"})
        star = star.get_text() if star else "None"

        # Extract the Rating
        rating = soup.find("span", attrs={"class": "a-size-base s-underline-text"})
        rating = rating.get_text() if rating else "None"

        # Append the extracted data to the dictionary
        d["title"].append(title)
        d['price'].append(price)
        d["link"].append(link)
        d["MRP"].append(mrp)
        d["Free Delivery"].append(free_delivery)
        d["Star"].append(star)
        d["Rating"].append(rating)

    except Exception as e:
        print(f"Error processing file {file}: {e}")

# Check if all lists are the same length
lengths = {key: len(value) for key, value in d.items()}
print("Lengths of each list:", lengths)

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data=d)

# Create an Excel workbook and sheet using openpyxl
wb = Workbook()
ws = wb.active
ws.title = "Amazon Data"

# Write the headers to the Excel sheet
ws.append(df.columns.tolist())

# Write the DataFrame to the Excel sheet row by row
for row in dataframe_to_rows(df, index=False, header=False):
    ws.append(row)

# Convert the 'link' column to actual hyperlinks in the Excel sheet
for i, cell in enumerate(ws['C'], start=2):  # Start from row 2 to skip the header
    if cell.value:  # If the cell has a value
        cell.hyperlink = cell.value  # Set the hyperlink
        cell.value = "link"  # Display text for the hyperlink
        cell.style = "Hyperlink"

# Save the Excel file
wb.save("data.xlsx")

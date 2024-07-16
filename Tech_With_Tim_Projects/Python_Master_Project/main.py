import pandas as pd
import csv
from datetime import datetime

class CSV:
    CSV_FILE="finance_data.csv"
    CLOUMNS=["date","amount","category","description"]

    @classmethod
    def intialize_csv(cls) -> None:
        try:
            pd.read_csv(cls.CSV_FILE) 
        except FileNotFoundError:
            df= pd.DataFrame(columns=["date","amount","category","description"]) 
            df.to_csv(cls.CSV_FILE,index=False)                
    
    @classmethod
    def add_entry(cls,date:str,amount:int,category:str,description:str) -> str :
        new_entry={
            "date":date,
            "amount":amount,
            "category":category,
            "description":description
            
        }
        with open(cls.CSV_FILE,"a",newline="") as csv_file :
            writer=csv.DictWriter(csv_file,fieldnames=cls.CLOUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")
if __name__ =='__main__':    
    CSV.intialize_csv()     
    CSV.add_entry("20-07-2024",1234,"Income","This is my income")
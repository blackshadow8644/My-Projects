import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount,get_category,get_date,get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE="finance_data.csv"
    CLOUMNS=["date","amount","category","description"]
    FORMAT="%d-%m-%Y"


    @classmethod
    def intialize_csv(cls) -> None:
        try:
            pd.read_csv(cls.CSV_FILE) 
        except FileNotFoundError:
            df= pd.DataFrame(columns=["date","amount","category","description"]) 
            df.to_csv(cls.CSV_FILE,index=False)                
    
    @classmethod
    def add_entry(cls,date:str,amount:float,category:str,description:str) -> str :
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

    @classmethod
    def get_transactions(cls,start_date:str,end_date:str) -> None:
        df=pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format=CSV.FORMAT)
        start_date=datetime.strptime(start_date,CSV.FORMAT) 
        end_date=datetime.strptime(end_date,CSV.FORMAT) 

        mask=(df["date"] >=start_date) & (df["date"]<=end_date)
        filtered_df=df.loc[mask]
        
        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            print(f"Transaction from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)} ")
            print(
                filtered_df.to_string(
                    index=False,formatters={"date":lambda x:x.strftime(CSV.FORMAT)}
                ))
            
            total_income=filtered_df[filtered_df["category"]=="Income"]["amount"].sum()
            total_expense=filtered_df[filtered_df["category"]=="Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Totoal Income: ${total_income:.2f}")
            print(f"Totoal Expense: ${total_expense:.2f}")
            print(f"Net saving: ${(total_income- total_expense):.2f}")
            
        return filtered_df



def add():
    CSV.intialize_csv()
    date=get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True
        )
    amount=get_amount()
    category=get_category()
    description=get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transaction(df):
    df.set_index('date', inplace=True)
    
    income_df = (df[df["category"] == "Income"]
                 .resample("D")
                 .sum()
                 .reindex(df.index, fill_value=0)
                )
    
    expense_df = (df[df["category"] == "Expense"]
                  .resample("D")
                  .sum()
                  .reindex(df.index, fill_value=0)
                 )
    
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")  # corrected expense_df here
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

    
    
def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transaction and summary within a date range")
        print("3.Exit")
        choice=input("Enter you choice (1-3): ")
        if choice =="1":
            add()
        elif choice =="2":
            start_date=get_date("Enter the start date (dd-mm-yyyy)")
            end_date=get_date("Enter the end date (dd-mm-yyyy)")
            df=CSV.get_transactions(start_date,end_date)
            if input("Do you want to see graph? (y/n) ").lower()=="y":
                plot_transaction(df)

        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")
            
if __name__ =='__main__':
    main()
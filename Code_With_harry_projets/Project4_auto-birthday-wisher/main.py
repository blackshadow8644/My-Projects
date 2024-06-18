import datetime
import pandas as pd
import smtplib

Gmail_ID=''
Gmail_PSWD=''

def sendEmail(to,sub,msg):
    print(f"Email to {to} sent with subject: {sub} and massage {msg}")
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(Gmail_ID,Gmail_PSWD)
    s.sendmail(Gmail_ID,to,f"Subject:{sub}\n\n{msg}")
    s.quit
    

if __name__ =='__main__':
    # exit()
    df=pd.read_excel("data.xlsx")
    # print(df)
    today=datetime.datetime.now().strftime("%d-%m")
    Yearnow=datetime.datetime.now().strftime("%Y")
    # print(today)
    
    df = pd.read_excel("data.xlsx", dtype={'Year': str})  # Specify string type for 'Year'
    
    # print(type(today))
    writeind=[]
    for index , item in df.iterrows():
        # print(index, item["Birthday"])
        bday=item["Birthday"].strftime("%d-%m")
        # print(bday)
        if (today==bday) and Yearnow not in  str(item["Year"]):
            sendEmail(item["Email"],"Happy Birthday",item["Dialogue"])
            writeind.append(index)
    # print(writeind)
    for i in writeind:
        yr=df.loc[i,"Year"]
        # print(yr)
        df.loc[i, 'Year',] = str(yr) + "," + str(Yearnow) , # Explicit casting (preferred)
# print(df)
df.to_excel('data.xlsx',index=False)
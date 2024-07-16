from datetime import datetime

def get_date(prompt,allow_default=False):
    date_str=input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")
    
def get_amount():
    pass

def get_category():
    pass

def get_description():
    pass
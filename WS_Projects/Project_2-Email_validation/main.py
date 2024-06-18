email=input("Enter email")
if len(email)>=6:
    if email[0].isalpha():
        if ("@"in email) and (email.count("@")==1):
            pass
        else:
            print("Wromg Email 3 ")
    else:
        print("Wromg Email 2 ")
else:
    print("Wromg Email 1 ")














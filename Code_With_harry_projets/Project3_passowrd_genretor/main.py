import string as sta
import random as rd
if __name__ =='__main__':
    s1=sta.ascii_lowercase
    # print(s1)
    s2=sta.ascii_uppercase
    # print(s2)
    s3=sta.digits
    # print(s3)
    s4=sta.punctuation
    # print(s4)
    plen=(input("Enter password length:\n"))
    x=[z for z in range (95)]
    # print(x)
    
    plen=int(input("Enter password length"))
    s=[]
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))
    # print(s)
    print(type(plen))
    # rd.shuffle(s)
    if type(plen)==int:
        pswd="".join(rd.sample(s,plen))
    # print("".join(s[0:plen]))
        print(pswd)
    
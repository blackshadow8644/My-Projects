def fiboiter(n):
    prenum=0
    curnrent=1
    for i in range(1,n):
        preprenum=prenum
        prenum= curnrent
        curnrent=prenum+preprenum
    return curnrent
def fiboRecur(n):
    if n==0:
        return  0
    elif n==1:
        return 1
    else:
        return fiboRecur(n-1)+fiboRecur(n-2)



if __name__ =='__main__':
    num=int(input("Enter Number\n"))
    print(f"Value of FibRec {fiboiter(num)}")
    print(f"Value of FibRec {fiboRecur(num)}")
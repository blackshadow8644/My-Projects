def Arm_num(n):
    sum=0
    order=len(str(n))
    copy_n=n
    while n > 0:
        digit = num%10
        sum+= digit**order
        num= num//10
        
    if sum==copy_n:
        print(f"{copy_n} is Armstrong number")
        return "True"
    else:
        print(f"{copy_n} is not Armstrong number")
        return "False"
    
Arm_num(31)
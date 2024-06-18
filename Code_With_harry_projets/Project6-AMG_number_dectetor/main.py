def Arm_num(num):
    sum=0
    order=len(str(num))
    copy_num=num
    while num > 0:
        digit = num%10
        sum+= digit**order
        num= num//10
        
    if sum==copy_num:
        return print(f"{copy_num} is Armstrong number")
    else:
        return print(f"{copy_num} is not Armstrong number")
        
Arm_num()
def sum(a,b):
    return a+b

def avg(a,b):
    return (a+b)/2
def Arm_num(num):
    sum=0
    order=len(str(num))
    copy_num=num
    while num > 0:
        digit = num%10
        sum+= digit**order
        num= num//10
        
    if sum==copy_num:
        print(f"{copy_num} is Armstrong number")
        return True
    else:
        print(f"{copy_num} is not Armstrong number")
        return False
Arm_num(41)
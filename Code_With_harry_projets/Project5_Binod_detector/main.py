import os
a="Abdullah"
def isBinod(filename):
    with open(filename,"r") as f:
        filecontent=f.read()
        print(filecontent)
        if a in filecontent.lower():
            return True
        else:
            return False
if __name__ =='__main__':   
    dir_contents=os.listdir()
    nBinod=0
    for i in dir_contents:
        if i.endswith(".txt"):
            print(f"Detecting {a} in {i}")
            flag=isBinod(i)
            if(flag):
                print(f"{a} Found in {i}")
                nBinod+=1
            else:
                print(f"{a} Not Found in {i}")
    print(f"******{a} Detector Summry******")
    print(f"{nBinod} files found with hidden {a} into them")
    input("Press Enter  button for exit:\n")
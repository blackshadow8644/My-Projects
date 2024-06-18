import time
from plyer import notification
import os
index=0
if __name__ == '__main__':
        while True:
                index +=1
                if index ==1:
                        os.system("pythonw ./main.py")
                notification.notify(
                title="**Please Drink Water Now!! ",
                message="The National Academies of Sciences, Engineering, and Medicine of the United States determined that an adequate daily fluid intake for men is approximately 15.5 cups (3.7 liters) and for women approximately 11.5 cups (2.7 liters).",
                app_icon=r"D:\New_Programing\Projects_python_Practise\Project2\icon.ico",
                timeout=12
    )
                time.sleep(60*60)
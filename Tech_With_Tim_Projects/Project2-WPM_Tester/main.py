import random
import curses
from curses import wrapper
import time


def start_screen(std):
    std.clear()
    std.addstr("Welcome to speed typing test")
    std.addstr("\nPress any key to begin:\n")
    std.refresh()

    std.getkey()



def diplay_text(std,target,curren,wpm=0):
    std.addstr(target)
    std.addstr(10, 10,  f"WPM: {wpm}")
        
        
    for i, char in enumerate(curren):
        correct_char=target[i]
        color=curses.color_pair(1)
        if char !=correct_char:
            color=curses.color_pair(3)
        
        std.addstr(0,i,char,color)



def load_text():
    with open("text.txt","r") as f:
        lines=f.readlines()
        return random.choice(lines).strip()

def wpm(std):
    target_text=load_text()
    curren_text=[]
    wpm=0
    start_time=time.time()
    std.nodelay(True)

    
    
    while True:
        
        time_elasped= max(time.time() - start_time,1)
        wpm=round((len(curren_text) / (time_elasped / 60)) / 5)
        
        
        std.clear()
        diplay_text(std,target_text,curren_text,wpm)
        std.refresh()
        
        if "".join(curren_text) == target_text:
            std.nodelay(False)
            break 
        
        try: 
            key=std.getkey()
        except:
            continue
        if ord(key) ==27:
            break
        if key in ("KEY_BACKSPACE",'\b',"\x7f"):
            if len(curren_text)>0:
                curren_text.pop()
        elif len(curren_text) < len(target_text):
            curren_text.append(key)
            
            
def main(std):
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
    
    start_screen(std)
    while True:
        wpm(std)
        std.addstr(2,0,"You completed the text! Press any key to continue...")
        key = std.getkey()
        if ord(key) == 27:
            break
wrapper(main)
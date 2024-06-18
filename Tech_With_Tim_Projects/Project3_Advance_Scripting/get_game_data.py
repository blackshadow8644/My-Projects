import os
import json
import shutil
from subprocess import PIPE,run
import sys



Game_Dir_Pattern="game"


def find_all_game_Paths(source):
    game_path=[]
    for root,dirs,filies in os.walk(source):
        for direcory in dirs:
            if Game_Dir_Pattern in direcory.lower():
                path=os.path.join(source,direcory)
                game_path.append(path)
        
        break
    return game_path


def get_name_form_path(paths,to_strip):
    new_name=[]
    for path in paths:
        


def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)



def main(sorce,target):
    cwd=os.getcwd()
    source_path=os.path.join(cwd,source)
    target_path=os.path.join(cwd,target)
    
    game_path=find_all_game_Paths(source_path)
    
    create_dir(target_path)
    
    


if __name__ =='__main__':
    args=sys.argv
    if len(args)!=3:
        raise Exception("You must pass a source and targer directory - only .")
    source,target=args[1:]
    main(source,target)
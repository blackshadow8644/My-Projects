import os 
def createIfNotExist (args) :
    if not os.path.exists(args) :
        os.mkdir(args)


files=os.listdir()
files.remove("main.exe")
if   os.path.exists("main.py"):
    files.remove("main.py")# print(files)
createIfNotExist("images")
createIfNotExist("Docs")
createIfNotExist("Media")
createIfNotExist("Others")
createIfNotExist("Zi")
imgExts=[".png",".jpeg",".jpg"]
images=[file for file in files if os.path.splitext(file)[1].lower() in imgExts]
docExts= [ ".txt",".docx",".doc",".pdf"]
docs=[file for file in files if os.path.splitext(file)[1].lower() in docExts]
zipsExt=[".zip",".rar"]
zip=[file for file in files if os.path.splitext(file)[1].lower() in zipsExt]
# print(images)
# print(docs)
mediaExt=[".mp4",".mp3",".flv",".mkv"]
medias=[file for file in files if os.path.splitext(file)[1].lower() in mediaExt]
others=[]
for file in files:
    ext= os.path.splitext(file)[1].lower()
    if  (ext not in imgExts) and (ext not in docExts) and (ext not in mediaExt) and(ext not in zipsExt) and os.path.isfile(file):
        others.append(file)


def move(folder,files_name):
    for file in files_name:
        os.replace( file,f"{folder}/{file}")

move("Docs",docs)
move("Others",others)
move("images",images)
move("Media",medias)
move("Zip",zip)

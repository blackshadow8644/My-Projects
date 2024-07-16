from pytube import YouTube
import tkinter as  tk
from tkinter import filedialog

def download_video(url,save_path):
    try:
        yt = YouTube(url)
        streams=yt.streams.filter(progressive=True,file_extension="mp4")
        highest_res_stream=streams.get_highest_resolution()
        highest_res_stream.download(output_path=save_path)
        print("Video download Succsesfully!")
    except Exception as e:
        print(e)
        
def open_file_dilog():
    folder=filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
        
    return folder



if __name__ =='__main__':
    root=tk.Tk()
    root.withdraw() 
    
    video=input("Please enter a Youtube url:\n")
    
    
    save=open_file_dilog()
    
    if  save:
        print("Download Started...")
        download_video(video,save)    
    else:
        print("Invalid save location.")
from pytube import YouTube
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
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
    root=Tk()
    root.geometry("644x344")
    # Heading
    Label(root,text="Free Youtube VIedo Downloader",font="comicsansms 13 bold",pady=15,fg="Red").grid(row=0,column=7)
    
    
# Text for out form
    name=Label(root,text="URl")
    # Pack text for out form
    name.grid(row=2,column=6)

    # Tkinter varible for storing entries
    name_value=StringVar()
    phone_value=StringVar()
    Gender_value=StringVar()
    Emergeny_value=StringVar()
    Payment_value=StringVar()
    Foodservicevalue=IntVar()

    # Enteries for a form
    nameentry=Entry(root,textvariable=name_value)


    # Packing Enteries
    nameentry.grid(row=10,column=6)
    # Checkbox & packing it

    # Button & packing it and assigning it a command
    Button(text="Download").grid(row=7,column=3)

    
    
    root.mainloop()
    
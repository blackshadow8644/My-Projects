import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from pytube import YouTube

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    progress_bar['value'] = int(percentage_of_completion)
    progress_label['text'] = f"Downloading... {int(percentage_of_completion)}%"


def download_video(url, save_path, custom_name):
    try:
        yt = YouTube(url, on_progress=on_progress)
        streams = yt.streams.filter(progressive=True, file_extension="mp4")
        highest_res_stream = streams.get_highest_resolution()

        filename = f"{save_path}/{custom_name}.mp4"
        highest_res_stream.download(output_path=filename)
        print("Video download successful!")
        progress_label['text'] = "Download complete!"

    except Exception as e:
        print(f"Error downloading video: {e}")
        progress_label['text'] = "Download failed!"

def open_file_dialog():
    folder = filedialog.askdirectory()
    if folder:
        print(f"Selected folder: {folder}")
        location.delete(0, tk.END)
        location.insert(0, folder)
    else:
        print("No folder selected.")

def set_placeholder(entry, placeholder):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground='white')

    def on_focus_out(event):
        if not entry.get():
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.configure(foreground='#AAAAAA')

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    entry.insert(0, placeholder)
    entry.configure(foreground='#AAAAAA')

def download_video_callback():
    url_val = url.get()
    location_val = location.get()
    name_val = name.get()
    if url_val and location_val:
        download_video(url_val, location_val, name_val)
    else:
        print("Please enter URL and location.")

window = ttk.Window(themename='darkly')
window.title("Youtube Video Downloader")
window.geometry("800x500")

title = ttk.Label(master=window, text="Youtube Video Downloader", font="Calibri 24 bold", foreground="#FF69B4")
title.pack(pady=20)

input_frame = ttk.Frame(master=window, padding=10, relief='groove', borderwidth=2)

url_label = ttk.Label(master=input_frame, text="Enter URL:", font="Calibri 14", foreground="#33CC33")
url_label.pack()

url = ttk.Entry(master=input_frame, width=40, font="Calibri 12", foreground="#FFFFFF", background="#333333")
set_placeholder(url, "Enter YouTube video URL")
url.pack(fill=tk.X, padx=10, pady=10)

name_label = ttk.Label(master=input_frame, text="Enter Name (optional):", font="Calibri 14", foreground="#33CC33")
name_label.pack()

name = ttk.Entry(master=input_frame, width=40, font="Calibri 12", foreground="#FFFFFF", background="#333333")
set_placeholder(name, "Enter Name for saving")
name.pack(fill=tk.X, padx=10, pady=10)

location_label = ttk.Label(master=input_frame, text="Enter location or Browse:", font="Calibri 14", foreground="#33CC33")
location_label.pack()

location = ttk.Entry(master=input_frame, width=40, font="Calibri 12", foreground="#FFFFFF", background="#333333")
set_placeholder(location, "Enter location or Browse")
location.pack(fill=tk.X, padx=10, pady=10)

browset_button = ttk.Button(
    master=input_frame,
    text='Browse Folder',
    command=open_file_dialog,
    style='primary.TButton'
)
browset_button.pack(padx=0, pady=0, side=tk.RIGHT, anchor=tk.E)

download_button = ttk.Button(
    master=input_frame,
    text='Download Video Now',
    command=download_video_callback,
    style='success.TButton'
)
download_button.pack(fill=tk.X, padx=10, pady=10)

input_frame.pack(pady=20)

style = ttk.Style()
style.configure('primary.TButton', foreground='white', background='#007bff')
style.configure('success.TButton', foreground='white', background='#28a745')

progress_frame = ttk.Frame(master=window)
progress_frame.pack(pady=20)

progress_label = ttk.Label(master=progress_frame, text="Ready to download...", font="Calibri 14", foreground="#FF69B4")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(master=progress_frame, orient='horizontal', length=400, mode='determinate')
progress_bar.pack(pady=10)

window.mainloop()
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from pytube import YouTube
import os

def download_video(url, save_path, custom_name, progress_var):
    try:
        yt = YouTube(url)
        print("Donwalod started")
        streams = yt.streams.filter(res="144p")
        highest_res_stream = streams.first()  # Get the first stream (highest resolution)

        filename = f"{save_path}/{custom_name}.mp4"
        highest_res_stream.download(output_path=filename, filename=custom_name, callback=progress_callback)
        print("Video download successful!")

    except Exception as e:
        print(f"Error downloading video: {e}")

def progress_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progress = (bytes_downloaded / total_size) * 100
    print(f"Download progress: {progress:.1f}%")

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
        # Create a progress bar
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(master=window, orient=tk.HORIZONTAL, length=300, mode='determinate', variable=progress_var)
        progress_bar.pack(pady=10)

        download_video(url_val, location_val, name_val, progress_var)
    else:
        print("Please enter URL and location.")

window = ttk.Window(themename="cyborg")  # Create the main window
window.title("Youtube Video Downloader")
window.geometry("800x500")

# Apply ttkbootstrap theme
ttk.Style(theme='darkly').theme_use()

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

browse_button = ttk.Button(
    master=input_frame,
    text='Browse Folder',
    command=open_file_dialog,
    style='primary.TButton'
)
browse_button.pack(padx=0, pady=0, side=tk.RIGHT, anchor=tk.E)

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

output_string = tk.StringVar()
output_label = ttk.Label(
    master=window,
    text="Output:",
    font="Calibri 24 bold",
    textvariable=output_string,
    foreground="#FF69B4"
)
output_label.pack(pady=20)

window.mainloop()

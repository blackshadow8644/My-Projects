import pyautogui
import numpy as np
from win32api import GetSystemMetrics
import time
import cv2

# Obtain real PC screen resolution
width, height = GetSystemMetrics(0), GetSystemMetrics(1)
dim = (width, height)

# Use the H.264 codec for high-quality video
f = cv2.VideoWriter_fourcc(*"XVID")

# Set the output video file with 60 FPS and the screen resolution dimensions
output = cv2.VideoWriter("test.mp4", f, 60.0, dim)

now_Time = time.time()
dur = 10  # Duration of the video in seconds
end_time = now_Time + dur

while True:
    image = pyautogui.screenshot()
    frame = np.array(image)

    # Convert the frame color from BGR to RGB
    colour = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    output.write(colour)
    
    C_time = time.time()
    if C_time > end_time:
        break

output.release()

print("---End---")

from pytube import YouTube

# Replace 'youtube_video_url' with the URL of the video you want to download
youtube_url = 'https://www.youtube.com/watch?v=r6zIGXun57U'

try:
    # Create a YouTube object
    yt = YouTube(youtube_url)

    # Get the highest resolution stream
    stream = yt.streams.get_highest_resolution()

    # Download the video
    stream.download()

    print('Video downloaded successfully.')

except Exception as e:
    print('Failed to download the video:', e)

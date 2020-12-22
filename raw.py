from pytube import YouTube

def youtubeDownload():
    link = input("Youtube link: ")
    yt = YouTube(link)
    video = yt.streams.first()

    video.download()
    print("complete")

youtubeDownload()
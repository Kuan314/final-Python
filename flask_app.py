from flask import Flask, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def form():
    return """
        <html>
            <head>
                <title>YouTube Downloader</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>
                <h1>Youtube Downloader</h1>

                <form action="/transform" method="post" enctype="multipart/form-data">
                    <label for="data_file">Please enter a valid Youtube URL:</label>
                    <input type="url" name="data_file" />
                    <br>
                    <input type="radio" id="mp4" name="format" value="mp4">
                    <label for="mp4">Mp4</label>
                    <input type="radio" id="mp3" name="format" value="mp3">
                    <label for="mp3">Mp3</label>
                    <br><br>
                    <input type="submit" value="Convert" />
                    <br><br>
                    <p>Please copy the YouTube link and paste to the column.</p>
                    <p>The video shoulld less than 15min.</p>
                    <p>After submit, just wait it. The download speed depands on your network.</p>
                    <p>The video name should NOT have some special icon.</p>
                    <p>Thank You!!</p>
                </form>
            </body>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():

    link = request.form['data_file']
    format = "mp4"
    format = request.form['format']

    if link.find('https://youtu.be'):
        link.replace('https://youtu.be', 'https://www.youtube.com')
    if link.find('https://m.youtube'):
        link.replace('https://m.youtube', 'https://www.youtube.com')

    try:
        yt = YouTube(link)
    except:
        return "link error"

    name = yt.title
    if  name.find('|'):
        name.replace('| ', '')

    if int(yt.length) <= 900:
        if format == 'mp4':
            yt.streams.get_by_itag('137').download('/home/KuanLim/mysite/Download/')
            name = name + '.mp4'
        else:
            yt.streams.get_by_itag('140').download('/home/KuanLim/mysite/Download/')
            os.rename(r'/home/KuanLim/mysite/Download/' + name + '.mp4', r'/home/KuanLim/mysite/Download/' + name + '.mp3')
            name = name + '.mp3'
    else:
        return "The video is too long, please try again."

    try:
        path = '/home/KuanLim/mysite/Download/' + name
    except:
        return "The name is not support for download, sorry."

    try:
        return send_file(path, as_attachment=True)
    except:
        return "File not found!"

if __name__ == '__main__':
    app.run()
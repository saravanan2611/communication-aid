import urllib.request
import pyrebase

import datetime
import time

global end,db,my_stream

def stream_handler(message):
    print(message["data"])
    download_image(message["data"])

def download_image(url):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print(timestamp)
    fullname = "drawn/image_"+timestamp+".png"
    urllib.request.urlretrieve(url,fullname)



config = {
  "apiKey": "AIzaSyBbQO1UjJzHOI-KRRwJZdM9yH6Qeq0h6mA",
  "authDomain": "eazycom-ce1d8.firebaseapp.com",
  "databaseURL": "https://eazycom-ce1d8.firebaseio.com",
  "storageBucket": "eazycom-ce1d8.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

my_stream = db.child("Server").child("abc").stream(stream_handler)
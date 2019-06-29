from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils
import cv2
from imutils.paths import list_images
import pyrebase

import datetime
import time
import os

global end,db

def process(file):
    start = time.time()
    print(file)
    time.sleep(0.3) #in seconds
    image = cv2.imread("drawn/"+file)
    orig = image.copy()
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	
    # pre-process the image for classification
    image = cv2.resize(image, (150, 150))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    a = [0] * 12
    # classify the input image
    (a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11]) = model.predict(image)[0]

    # build the label
    label=0
    label2=0
    label3=0
    label4=0  
    for i in range(12):
    	print(a[i])

    
    for i in range(11):
    	if(a[label]<a[i+1]):
    		label4=label3    		
    		label3=label2
    		label2=label
    		label=i+1;
    	elif(a[label2]<a[i+1]):
    		label4=label3
    		label3=label2
    		label2=i+1
    	elif(a[label3]<a[i+1]):
    		label4=label3
    		label3=i+1
    	elif(a[label4]<a[i+1]):
    		label4=i+1 

    print(label,label2,label3,label4) 
    print("\n\n")

    proba  = a[label]
    proba2 = a[label2]
    proba3 = a[label3]
    proba4 = a[label4]

    dict = ["one", "two", "three", "yes",  "no","up","down","left","right", "sos","zzz","money"]

    label  = dict[label]
    label2 = dict[label2]
    label3 = dict[label3]
    label4 = dict[label4]

    output_db = db.child("Client").child("abc").update({"label1": label,"label2": label2, "label3": label3,"label4": label4 })
    print(output_db)

    """
    label = "help" if help > nothelp else "nothelp"
    proba = help if help > nothelp else nothelp
    """

    label = "{}: {:.2f}%".format(label, proba * 100)
    label2 = "{}: {:.2f}%".format(label2, proba2 * 100)
    label3 = "{}: {:.2f}%".format(label3, proba3 * 100)
    label4 = "{}: {:.2f}%".format(label4, proba4 * 100)

    # draw the label on the image
    output = imutils.resize(orig, width=400)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
    	0.7, (0, 255, 0), 2)
    cv2.putText(output, label2, (10, 50),  cv2.FONT_HERSHEY_SIMPLEX,
    	0.7, (0, 255, 0), 2)
    cv2.putText(output, label3, (10, 75),  cv2.FONT_HERSHEY_SIMPLEX,
    	0.7, (0, 255, 0), 2)
    cv2.putText(output, label4, (10, 100),  cv2.FONT_HERSHEY_SIMPLEX,
    	0.7, (0, 255, 0), 2)

    # show the output image
    # cv2.imshow("Output", output)
    end = time.time()
    print("Processing Time: ",end-start)
    return

dic= [x for x in os.listdir('drawn') if x.endswith('.png')]
print(len(dic))
lend=len(dic)

config = {
  "apiKey": "AIzaSyBbQO1UjJzHOI-KRRwJZdM9yH6Qeq0h6mA",
  "authDomain": "eazycom-ce1d8.firebaseapp.com",
  "databaseURL": "https://eazycom-ce1d8.firebaseio.com",
  "storageBucket": "eazycom-ce1d8.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# load the trained convolutional neural network
print("[INFO] loading network...")
model = load_model("draw.model")

while True:
	dict=[x for x in os.listdir('drawn')]
	temp=len(dict)
	if temp<lend:
		lend=temp
	elif temp>lend:
		lend=temp
		print(lend)
		print(dict)
		file=dict[temp-1]
		process(file)
		print("done")
	if len(dict)==lend:
		continue
	print(dict)

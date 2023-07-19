import requests
import cv2
import numpy as np
import imutils
import cv2
import os
url = "http://10.5.220.164:8080/shot.jpg"
video = cv2.VideoCapture(url)
facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
count=0
nameID=str(input("Enter Your Name: ")).lower()
path='images/'+nameID
isExist=os.path.exists(path)
if isExist:
    print("Name Already Taken")
    nameID=str(input("Enter Your Name Again: ")).lower()
else:
    os.makedirs(path)
while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=1000, height=1800)
    faces=facedetect.detectMultiScale(img,1.3,5)
    for x,y,w,h in faces:
        count=count+1
        name='./images/'+nameID+'/'+str(count)+'.jpg'
        print("Creating Images....."+name)
        cv2.imwrite(name,img[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w+1,y+h+1),(0,255,0),5)
    cv2.imshow("WindowFram", img)
    cv2.waitKey(1)
    if count>500:
        break
video.release()
cv2.destroyAllWindows()

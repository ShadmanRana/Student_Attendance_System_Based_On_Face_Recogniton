import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from keras.models import load_model
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
font=cv2.FONT_HERSHEY_COMPLEX
model = load_model('keras_model.h5')
def get_className(classNo):
    if classNo==0:
        return "shojib"
    elif classNo==1:
        return "rana"
while True:
    success, imgOrginal=cap.read()
    faces=facedetect.detectMultiScale(imgOrginal,1.3,5)
    for x,y,w,h in faces:
        crop_image=imgOrginal[y:y+h,x:x+w]
        img=cv2.resize(crop_image,(224,224))
        img=img.reshape(1,224,224,3)
        prediction=model.predict(img)
        classIndex=np.argmax(model.predict(img), axis=-1)
        probabilityValue=np.amax(prediction)
        if classIndex==0:
            cv2.putText(imgOrginal, "SHOJIB", (x, y-10), font, 0.75, (255,0,0), 1, cv2.LINE_AA)
        elif classIndex==1:
            cv2.putText(imgOrginal, "forhad", (x, y-10), font, 0.75, (0,255,0), 1, cv2.LINE_AA)
        elif classIndex==2:
            cv2.putText(imgOrginal, "jahirul", (x, y-10), font, 0.75, (0,255,0), 1, cv2.LINE_AA)
        cv2.putText(imgOrginal, str(round(probabilityValue*100,2))+"%", (180, 75), font, 0.75, (0,255,0), 1, cv2.LINE_AA)
    cv2.imshow("Result", imgOrginal)
    k=cv2.waitKey(1)
    if k==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
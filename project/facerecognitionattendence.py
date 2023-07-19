#! /usr/bin/env python3
import face_recognition as fr
import cv2
import subprocess
from getpass import getpass
import numpy as np
import os
from datetime import date
import mysql.connector
import imutils
import requests
def check_sudo_password_required():
	try:
		subprocess.check_output("sudo -n -v",shell=True)
		return False
	except subprocess.CalledProcessError:
		return True
password_required=check_sudo_password_required()
command='sudo -S /opt/lampp/lampp start'
if password_required:
	p="rana"
	subprocess.run(command,shell=True,input=(p+'\n').encode(),check=True)
	print("1")
else:
	subprocess.run(command,shell=True,input=('rana'+'\n').encode(),check=True)
	print("0")
path='images'
images=[]
classname=[]
mylist=os.listdir(path)
print(mylist)
for cl in mylist:
	curImg=cv2.imread(f'{path}/{cl}')
	images.append(curImg)
	classname.append(os.path.splitext(cl)[0])
id=0
total=0
def databaseconnet(name,todate):
	#establishing the connection
	conn = mysql.connector.connect(
	user='root', password='', host='127.0.0.1', database='facerecognition')

	#Creating a cursor object using the cursor() method
	cursor = conn.cursor()
	# Preparing SQL query to INSERT a record into the database.
	'''insert_stmt = (
		"INSERT INTO students(ID, NAME,Time)"
		"VALUES (%s, %s, %s)"
	)
	global id
	id=id+1
	data = (id, name, time)'''
	global id
	id=id+1
	global total
	if id==1:
		cursor.execute("SELECT total_attendance,total_class from students")
		Count=cursor.fetchall()
		print(Count[0][0])
		print(len(Count))
		dlen=len(Count)
		for i in range(dlen):
			total=Count[0][1]+1;
			percent=(Count[i][0]/total)*100
			percent=round(percent,3)
			if percent>=65:
				sql="UPDATE students SET total_class={},percentage={},student_status='{}' WHERE total_attendance={}".format(total,percent,'collegiate',Count[i][0])
				cursor.execute(sql)
				conn.commit()
			else:
				sql="UPDATE students SET total_class={},percentage={},student_status='{}' WHERE total_attendance={}".format(total,percent,'noncollegiate',Count[i][0])
				cursor.execute(sql)
				conn.commit()
	print(total)
	cursor.execute("SELECT attendance_date,percentage from students where id='{}'".format(name))
	selectsql=cursor.fetchall()
	select=selectsql[0][0]
	print(select)
	todate=str(todate)
	print(todate,type(select))
	if todate!=select:
		percent=1/total
		percent=(percent+selectsql[0][1]/100)*100
		percent=round(percent,2)
		print(percent)
		if percent>=65:
			sql="UPDATE students SET total_attendance=total_attendance+1,attendance_date='{}',percentage={},student_status='{}' WHERE id='{}'".format(todate,percent,'collegiate',name)
			cursor.execute(sql)
			conn.commit()
		else:
			sql="UPDATE students SET total_attendance=total_attendance+1,attendance_date='{}',percentage={},student_status='{}' WHERE id='{}'".format(todate,percent,'noncollegiate',name)
			cursor.execute(sql)
			conn.commit()
def findencodings(images):
	encodelist=[]
	for img in images:
		img=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encode=fr.face_encodings(img)[0]
		encodelist.append(encode)
	return encodelist
def markattendence(name):
	with open('Attendence.csv','r+') as f:
		mydatalist=f.readlines()
		namelist=[]
		for line in mydatalist:
			entry=line.split(',')
			namelist.append(entry[0])
		if name not in namelist:
			#now = datetime.now()
			todate=date.today();
			#print(todate)
			#dtstring=now.strftime('%H:%M:%S')
			databaseconnet(name,todate)
			#f.writelines(f'\n{name},{todate}')	
encodelistknown=findencodings(images)
print('Encoding Completes')
url = "http://100.108.83.134:8080/shot.jpg"
cap=cv2.VideoCapture(url)
while True:
	#success, img =cap.read()
	img_resp = requests.get(url)
	img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
	img = cv2.imdecode(img_arr, -1)
	img = imutils.resize(img, width=1000, height=1800)
	imgs=cv2.resize(img,(0,0),None,0.25,0.25)
	imgs=cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
	facescurframe=fr.face_locations(imgs)
	encodecurframe=fr.face_encodings(imgs,facescurframe)
	for encodeface,faceloc in zip(encodecurframe,facescurframe):
		matches=fr.compare_faces(encodelistknown,encodeface)
		facedis=fr.face_distance(encodelistknown,encodeface)
		dm=min(facedis)
		#print(dm)
		#print(facedis)
		matchindex=np.argmin(facedis)
		#print(matchindex)
		if matches[matchindex] and dm<0.45:
			name=classname[matchindex].upper()
			print(name)
			markattendence(name)
			y1,x2,y2,x1=faceloc
			y1,x2,y2,x1=4*y1,4*x2,4*y2,4*x1
			cv2.rectangle(img,(x1,y1,),(x2,y2),(0,255,0),2)
			cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
			cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
		else:
			y1,x2,y2,x1=faceloc
			y1,x2,y2,x1=4*y1,4*x2,4*y2,4*x1
			cv2.rectangle(img,(x1,y1,),(x2,y2),(0,255,0),2)
			cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
			cv2.putText(img,"Not found",(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
	cv2.imshow('webcam',img)
	if cv2.waitKey(1)==27:
		break
	if (cv2.getWindowProperty('webcam',0)<0):
		break;
cap.release()
cv2.destroyAllWindows()

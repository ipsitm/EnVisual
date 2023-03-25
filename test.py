from imageai.Detection import VideoObjectDetection
import os
import mysql.connector
import socket
from datetime import date
from datetime import datetime
import os
from twilio.rest import Client
import requests

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path , "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
detector.loadModel()

custom_objects = detector.CustomObjects(person=True, knife=True, scissors=True, backpack=True, skis=True)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
a=hostname
b=IPAddr

flag = 0

def crimeDetected(type):
	global flag
	today=date.today()
	c=today.strftime("%d/%m/%Y")
	now = datetime.now()
	d=now.strftime("%H:%M:%S")

	connection=mysql.connector.connect(
		host = "localhost",
		user = "Kavach_test",
		password = "kavach06",
		database = "test1"
	)
	cursor = connection.cursor()
	e=type
	f="High"
	sql="INSERT INTO Crime_Report(Device_Name, IP_Address,Date,Time,Type,Severity) VALUES (%s,%s,%s,%s,%s,%s)"
	val=(a,b,c,d,e,f)
	cursor.execute(sql,val)
	connection.commit()
	cursor.close()
	connection.close()
	
	if (type=="Murder"):
		flag=flag+1
	if (flag==1):

		ip_address = requests.get("https://ipinfo.io/ip").text.strip()

		response = requests.get(f"https://ipinfo.io/{ip_address}?token=bf5bdee159210e")

		data = response.json()
		location = data["loc"]
		city = data["city"]
		region = data["region"]
		country = data["country"]
		account_sid = "ACc826109e70e882e60ba810dfc41f6011"
		auth_token = "576f7f06c20ba6cdac64890697bf19ca"
		client = Client(account_sid, auth_token)

		message = client.messages \
    		.create(
         		body='Crime Detected ' + type + 'Date' + c + 'Time : ' + d+ f" IP address: {ip_address}" + f" Location: {location}" + f" City: {city}" + f" Region: {region}" + f" Country: {country}" ,
         		from_='+14754052684',
         		to='+917275652817'
     		)

		print(message.sid)
		
	

def forFrame(frame_number, output_array, output_count):
    #print("FOR FRAME " , frame_number)
    #print("Output for each object : ", output_array)
    #print("gap... : ")
    #print("Output count for unique objects : ", output_count)
    if(any(item['name'] == 'person') for item in output_array):
        if(any((item1['name']  == 'knife') or (item1['name']  == 'scissors') or (item1['name']  == 'backpack') or (item1['name']  == 'skis') for item1 in output_array)):
            crimeDetected("Murder")
    
    if(any(item['name'] == 'person') for item in output_array):
        if(any((item1['name']  == 'knife') for item1 in output_array)):
            crimeDetected("Murder")
		
    #for key in output_array:
        #print(key['name'])


    #if(('person' in output_array) and (('knife' in output_array) or ('scissors' in output_array))):
    #print("------------END OF A FRAME --------------")

video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "traffic.mp4"),
                                output_file_path=os.path.join(execution_path, "knife_detected")
                                , frames_per_second=20, per_frame_function=forFrame, custom_objects=custom_objects,log_progress=True)
print(video_path)
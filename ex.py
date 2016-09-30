# Data that the script must recieve


import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3('2016-05-20', api_key='885fc12f8c46a97bdd6dc53b9ec90e37f9b9b44f')
print("HELLO")

def add():
	js = visual_recognition.classify(images_url='https://pics.ae.com/is/image/aeo/0111_3522_888_f?$cat-main_small$')
	print(js)
	print()
	cl = js['images']
	for i in cl:
		for j in i['classifiers']:
			for k in j['classes']:
				type = k['class']
				#if(type=='clothing' or type=='fabric'):
				#ask for more details
				print(type)
	print()
	print(cl)
	#conditions to be put to ask the user to better define the item added

add()

#use weather data, travel duration 
#
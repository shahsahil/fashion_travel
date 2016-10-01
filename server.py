from flask import Flask, render_template, request, url_for
from flask import jsonify
import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3
visual_recognition = VisualRecognitionV3('2016-05-20', api_key='885fc12f8c46a97bdd6dc53b9ec90e37f9b9b44f')
import requests
import os

app = Flask(__name__)

js=[]
c=0
selected=[]
city=""
def visualapi(url):
	js = visual_recognition.classify(images_url=url)
	cl = js['images']
	for i in cl:
		for j in i['classifiers']:
			for k in j['classes']:
				type = k['class']
				if(type=='shirt' or type =='sneaker' or type=='jean'):
					return type
	print(j)
	return ""

def getweatherdata(pincode,countrycode):
	temp =0 #1-v cool  2- mix  3-hot
	l=[pincode,"%3A4%3A",countrycode]
	location = ''.join(l)
	r = requests.get('https://8ec8d584-1f3a-4b02-8cf5-eb3806a42be2:Mti7nn8dnq@twcservice.mybluemix.net/api/weather/v1/location/'+location+'/forecast/daily/7day.json')
	data = json.loads(r.text)['forecasts']
	for i in data:
		#print(i)
		max = i['max_temp']
		min = i['min_temp']
		try:
			short = i['day']['shortcast']
			p1 = short.find('sun')
			p2 = short.find('cloud')
			p3 = short.find('clear')
			if(min<68 and max<68):
				#very cold 
				temp=1
			elif(min<68 and max < 30):
				#cold and hot mix
				temp=2
			else:
				#summer
				temp=3
			if(p1!=-1):
				#sunny weather
				if(max>95):
					#carry umbrella to protect from heat
					print("v high")
				else:
					print("sunny")
			elif(p2!=-1):
				#cloudy weather
				print("Cloudy weather! Carry umbrella!")
			elif(p3!=-1):
				print("Very pleasant weather!")
			print("Temperature")
			print("Max", max)
			print("Min", min)
		except:
			print("Exception")
	return temp

def process(temp):
	#based on temp value we need to create an array of clothes which are selected
	#scan js to find the matching ones
	select=[]
	if(temp==1):
		cloth = 'cool'
	elif(temp==2):
		cloth = 'both'
	elif(temp==3):
		cloth = 'summer'
	print(cloth)
	for i in js:
		if(i['description'] == cloth or i['description'] == 'both'):
			select.append(i)
	return select
	
@app.route('/add', methods=['POST'])
def add():
	global c
	c+=1
	print("ADD")
	global js
	j=request.get_json()
	j=j['form']
	j['no']=c
	#currently only image url and number in the json 
	#run visual recognition api here to find the class
	t = visualapi(j['image'])
	j['title']= t
	js.append(j)
	print(j)
	return "0"

@app.route('/add2', methods=['POST'])
def add2():
	j=request.get_json()
	j=j['form']
	print(j)
	js[-1]['title'] = j['title']
	js[-1]['description'] = j['description']
	return "0"

@app.route('/travel', methods=['POST'])
def travel():
	global city
	city=""
	j=request.get_json()
	j=j['form']
	pincode = j['pincode']
	countrycode = j['countrycode']
	days = j['days']
	city = j['city']
	print(j)
	global selected
	selected = []
	temp = getweatherdata(pincode, countrycode)
	selected = process(temp)
	return "0"

@app.route('/last')
def get_last():
	l = [js[-1]]
	return jsonify(l)
	
@app.route('/all')
def get_all():
	print(js)
	return jsonify(js)

@app.route('/carry')
def carry():
	#will return the image urls
	return jsonify(selected)
	
@app.route('/carry2')
def carry2():
	api_key = "a9501184959ec1273e60288056cef5e638b7a0ef"
	global city
	print(city)
	city = city.strip()
	city = '%20'.join(city.split(' '))
	news=[]
	news_url ="https://access.alchemyapi.com/calls/data/GetNews?apikey="+api_key+"&return=enriched.url.title&start=1474675200&end=1475362800&q.enriched.url.enrichedTitle.entities.entity=|text="+ city +",type=city|&q.enriched.url.enrichedTitle.taxonomy.taxonomy_.label=news&count=25&outputMode=json"
	news_json = json.loads(requests.get(news_url).text)
	if(news_json['status'] =="OK"):
		news_json = news_json['result']['docs']
		for i in news_json:
			news.append(i['source']['enriched']['url'])
	#will return the news articles
	return jsonify(news)

# Run the server
if __name__ == '__main__':
	PORT = int(os.getenv('VCAP_APP_PORT', '80'))
	HOST = str(os.getenv('VCAP_APP_HOST', '0.0.0.0'))
	app.run( HOST , PORT)
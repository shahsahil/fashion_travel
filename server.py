from flask import Flask, render_template, request, url_for
from flask import jsonify
import json
app = Flask(__name__)

js=[]
@app.route('/hello', methods=['POST'])
def hello():
	print("hello")
	global js
	j=request.get_json()
	j=j['form']
	js.append(j)
	print(j)
	#add(js)
	#return render_template('form_action.html', name=name, email=email)
	return "0"
@app.route('/hell')
def get_hello():
	print(js)
	return jsonify(js)
# Run the server
if __name__ == '__main__':
	app.run( 
		host="0.0.0.0",
		port=int("80"))
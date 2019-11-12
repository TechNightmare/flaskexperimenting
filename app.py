from flask import Flask, render_template, request, redirect, Response
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'frank'
app.config['MYSQL_PASSWORD'] = 'supersicher'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':			#wenn Submit Button gedrueckt wird 
		#fetch form data
		userInfos = request.form
		username  = userInfos['username']
		email     = userInfos['email']

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email) Values(%s, %s)", (username, email))
		mysql.connection.commit()
		cur.close()
		return redirect('/users')

	return render_template('index.html')

@app.route('/users')
def users():
	cur = mysql.connection.cursor()
	count = cur.execute("SELECT * FROM users")	
	if count > 0:
		userInfos = cur.fetchall()
		items = []
		for row in userInfos:
			for key in cur.description:
				items.append({key[0]: value for value in row})

		print(json.dumps({'items': items}))
		return render_template('users.html', userInfos=userInfos)		# jinja template

#oder <int:name> falls etwas direkt gecasted werden soll
@app.route('/users/<name>')
def users_name(name):
	cur = mysql.connection.cursor()
	count = cur.execute("SELECT * FROM users WHERE name=%s", [name])	
	if count > 0:
		userInfos = cur.fetchall()
		return render_template('users.html', userInfos=userInfos)		# jinja template

@app.route('/testpost', methods=['GET', 'POST'])		#if statement isnt POST it is GET so last statement gets used
def foo():
	if request.method == 'POST':			#wenn Submit Button gedrueckt wird 
		#fetch form data
		request_data = request.data
		#je nach json nun die attributes auslesen
		username = request_data.get('Username')
		email = request_data.get('Email')

		#nun entsprechendes sql statement machen

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, email) Values(%s, %s)", (username, email))
		mysql.connection.commit()
		cur.close()

		#return nen response code
		return "hat jeklappt oder auch nicht"


	#dinge die getan werden wenns get ist
	return "get_request wurde angefragt"

@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def echo():
	if request.method == 'GET':
		return "ECHO: GET\n"

	elif request.method == 'POST':
		return "ECHO: POST\n"

	elif request.method == 'PATCH':
		return "ECHO: PATCH\n"

	elif request.method == 'PUT':
		return "ECHO: PUT\n"

	elif request.method == 'DELETE':
		return "ECHO: DELETE\n"

@app.route('/messages', methods=['POST'])
def message():
	if request.headers['Content-Type'] == 'application/json':
		return "Sie haben JSON Bullshit geschickt Sie Dreck :( " + json.dumps(request.json)

	return "Nix zu sehen hier\n"

@app.route('/response', methods=['GET'])
def response():
	#dictinaries are objects, arrays not
	data = {
		'name' : 'geht dich nichts an',
		'alter' : 42
	}
	js = json.dumps(data)											#json encoder
	resp = Response(js, status=200, mimetype='application/json')	#fuellt HTTP Header
	resp.headers['Link'] = 'hierkannmanwaseintragen.fuckya'

	return resp


if __name__ == '__main__':
	app.run(debug=True)

"""
Registrierung:
Vorname, Nachname, Username/Alias in Anwendung, Email, Passwort

Login
Username oder Email?, Passwort

Cursor --> Json

import json
items = [dict(zip([key[0] for key in cursor.description()], row)) for row in userInfos]
print(json.dumps({'items': items}))

CRUD - create, read, update, delete --> POST, GET, PUT, DELETE
response code?
"""
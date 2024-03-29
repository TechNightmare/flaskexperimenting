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
	#todo just do this once, evtl einfach start des python programms?
	cur = mysql.connection.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS users(name varchar(255), email varchar(255))")
	mysql.connection.commit()
	cur.close()
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
	if request.method == 'POST':			#wenn Submit Button gedrueckt wird, gilt nicht für json 
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

idcount = 0
@app.route('/messages', methods=['POST'])			#json geposted
def message():
	#ID zufügen und neue Spalte machen, Counter hochsetzen
	global idcount
	if request.headers['Content-Type'] == 'application/json':
		cur = mysql.connection.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS registration(id int, name varchar(255), username varchar(255), email varchar(255), password varchar(255))")
		mysql.connection.commit()
		cur.close()
		

		content 	= request.json
		print(content)
		name 		= content['name']		#auslesen
		username 	= content['username']
		email 		= content['email']
		password 	= content['password']

		idcount += 1

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO registration(id, name, username, email, password) Values(%s, %s, %s, %s, %s)", (idcount, name, username, email, password))
		mysql.connection.commit()
		cur.close()

		#return "Sie haben JSON Bullshit geschickt Sie Dreck :( " + json.dumps(request.json)
		
		return "Sie haben JSON Bullshit geschickt Sie Dreck :(ID: {id} Name: {name}  Username: {username}, Email: {email}, Password: {password}".format(id = idcount, name=name, username=username, email=email, password=password)
	return "Nix zu sehen hier\n"


@app.route('/response', methods=['GET'])			#json antwort
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
	app.run(host='0.0.0.0', debug=True)		#host angabe wichtig für docker

"""
Registrierung:

Passwörter gehashed speichern!!!
Name, Username in Anwendung, Email, Passwort

Login
Username oder Email?, Passwort

Cursor --> Json

import json
items = [dict(zip([key[0] for key in cursor.description()], row)) for row in userInfos]
print(json.dumps({'items': items}))


CRUD - create, read, update, delete --> POST, GET, PUT, DELETE

1. Registrierung 
	Paul schickt ein Post-Request mit JSON Daten für Neuregistrierung
	Check ob Username schon vergeben
	Check ob Mail-Adresse bereits verwendet
	ansonsten in DB einpflegen
	User-ID zurückgeben und Response Code OK

2. Login
	Paul schickt Get-Request mit Username/Email und Passwort
	Check ob User in DB
	Check ob Passwort übereinstimmt
	Rückgabe der User-ID und Response Code OK

3. Account löschen

4. Daten ändern



response code?
"""
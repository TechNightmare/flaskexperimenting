from flask import Flask, render_template, request, redirect, Response
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


#Registration
@app.route('/account/user', methods=['POST'])
def register():
	#todo just do this once, evtl einfach start des python programms?
	if request.headers['Content-Type'] == 'application/json':

		#create Table
		cur = mysql.connection.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS users(UserID int NOT NULL AUTO_INCREMENT, name varchar(255), username varchar(255), email varchar(255), password varchar(255), PRIMARY KEY (UserID))")
		mysql.connection.commit()
		cur.close()
		
		content 	= request.json
		#print(content)
		name 		= content['name']		#auslesen
		username 	= content['username']
		email 		= content['email']
		password 	= content['password']


		# create User in DB
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users(name, username, email, password) Values(%s, %s, %s, MD5(%s))", (name, username, email, password))
		mysql.connection.commit()

		#get ID
		cur = mysql.connection.cursor()
		cur.execute("SELECT UserID FROM users WHERE username=%s", [username])
		UserID = cur.fetchone()
		UserID = UserID[0]
		cur.close()

		data = {
		'UserID' : UserID
		}

		js = json.dumps(data)											#json encoder
		resp = Response(js, status=200, mimetype='application/json')	#fuellt HTTP Header
		
		return resp
	
	return "Iwas lief wohl schief\n"

# Login
@app.route('/account/user/login', methods=['POST'])
def login():
	#todo just do this once, evtl einfach start des python programms?
	if request.headers['Content-Type'] == 'application/json':

		
		content 	= request.json
		#print(content)
		username 	= content['username']
		password 	= content['password']

		# hier etwas rumhashen
		# hashes vergleichen

		#get row
		cur = mysql.connection.cursor()
		cur.execute("SELECT UserID, password FROM users WHERE username=%s", [username])
		userdata = cur.fetchone()
		cur.close()

		print(userdata)
		UserID = userdata[0]
		password_db = userdata[1]
		
		if password == password_db:
			data = {
			'UserID' : UserID
			}

		else:
			data = {
			'UserID' : "Not authorized" 
			}

		#http response code aendern

		js = json.dumps(data)											#json encoder
		resp = Response(js, status=200, mimetype='application/json')	#fuellt HTTP Header
		
		return resp
	
	return "Iwas lief wohl schief\n"

# Delete 
@app.route('/account/user/<id>', methods=['DELETE'])
def delete(id):
	#todo just do this once, evtl einfach start des python programms?
	if request.method == 'DELETE':

		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM users WHERE UserID=%s", id)
		mysql.connection.commit()

		return "Jelöscht du Lappen"

	
	return "Iwas lief wohl schief\n"



@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def echo():
	if request.method == 'GET':
		resp = Response("Echo: GET\n")
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

	elif request.method == 'POST':
		return "ECHO: POST\n"

	elif request.method == 'PATCH':
		return "ECHO: PATCH\n"

	elif request.method == 'PUT':
		return "ECHO: PUT\n"

	elif request.method == 'DELETE':
		return "ECHO: DELETE\n"


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
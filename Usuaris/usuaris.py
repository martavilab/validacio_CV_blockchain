from flask_cors import CORS

import sqlite3

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from hashlib import sha256


from flask import Flask, jsonify, request, render_template

import Crypto
import Crypto.Random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


import binascii


app = Flask(__name__)
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.route('/wallet/new', methods=['POST'])
def new_wallet():
	random_gen=Crypto.Random.new().read
	private_key=RSA.generate(1024, random_gen)
	public_key=private_key.publickey()

	mail=request.form['email']
	#comprovem/afegim la validesa del email amb db
	conn=sqlite3.connect('emails.db')
	c=conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS regEmails
            (adress text
            )""")
	conn.commit()
	c.execute("SELECT * FROM regEmails")
	emails=c.fetchall()
	for elem in emails:
		if elem[0]==mail:
			response={
				'private_key': 'ERROR',
				'public_key': 'ERROR'
			}
			return jsonify(response), 200
		else:
			pass

	c.execute("INSERT INTO regEmails VALUES (?)", (mail,))
	conn.commit()
	conn.close()

	#Afegim les claus a un db
	prk=str(binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'))
	puk=str(binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii'))
	conn=sqlite3.connect('entitats.db')
	c=conn.cursor()
	c.execute("""CREATE TABLE IF NOT EXISTS Entitats
	            (puk text,
		    	prk text,
		    	email text
	            )""")
	conn.commit()
	c.execute("INSERT INTO Entitats VALUES (?,?,?)", (puk,prk,mail))
	conn.commit()
	conn.close()

	response={
		'private_key': binascii.hexlify(private_key.export_key(format('DER'))).decode('ascii'),
		'public_key': binascii.hexlify(public_key.export_key(format('DER'))).decode('ascii')
	}
	return jsonify(response), 200

@app.route('/confirmar/entrada', methods=['POST'])
def confirm():
	entitat_public_key = request.form['entitat_public_key']
	entitat_private_key = request.form['entitat_private_key']
	usuari=request.form['usuari']
	if entitat_public_key==usuari:
		needsval=True
	else:
		needsval=False
	conn=sqlite3.connect('entitats.db')
	c=conn.cursor()
	c.execute("SELECT * FROM Entitats")
	entitats=c.fetchall()
	for elem in entitats:
		if elem[0]==entitat_public_key and elem[1]==entitat_private_key:
			email=elem[2]
			response={'bool':True, 'email': email, 'needsval':needsval}
			conn.close()
			return jsonify(response), 200



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=4002, type=int, help='port to listen to')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)

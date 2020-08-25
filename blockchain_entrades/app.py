import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request, render_template

import Crypto
import Crypto.Random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA


import binascii

from collections import OrderedDict

from blockchain_entrades import Entrada


import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
	return render_template('./home.html')

@app.route('/index')
def index():
	return render_template('./genwallet.html')

@app.route('/nova/entrada')
def make_entrada():
    return render_template('./nova_entrada.html')



@app.route('/veure/entrades')
def view_entrada():
    return render_template('./veure_entrades.html')




@app.route('/auth/cv', methods=['POST'])
def auth_cv():
	email=request.form['email']
	entitat_puk=request.form['entitat_puk']
	entitat_prk=request.form['entitat_prk']
	conn=sqlite3.connect('entitats.db')
	c=conn.cursor()
	c.execute("SELECT * FROM Entitats")
	entitats=c.fetchall()
	for elem in entitats:
		if elem[0]==entitat_puk and elem[1]==entitat_prk and elem[2]==email:
			conn.close()
			response = {'Response': 'Autoritzat'}
			return jsonify(response), 200
	response= {'Response': 'NO Autoritzat'}
	conn.close()
	return jsonify(response), 400

@app.route('/generate/entrada', methods=['POST'])
def generate_entrada():
	entitat_public_key = request.form['entitat_public_key']
	entitat_private_key = request.form['entitat_private_key']
	usuari = request.form['usuari']
	info = request.form['info']
	#creem objecte de la classe
	entrada = Entrada(entitat_public_key, entitat_private_key, usuari, info)
	response = {'entrada': entrada.to_dict(), 'signature': entrada.sign_entrada()}
	return jsonify(response), 200





if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=8081, type=int, help='port to listen to')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)

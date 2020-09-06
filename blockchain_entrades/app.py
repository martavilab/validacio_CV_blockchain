from flask import Flask, jsonify, request, render_template
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

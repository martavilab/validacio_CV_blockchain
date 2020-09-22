import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
from hashlib import sha256


from flask import Flask, jsonify, request, render_template, redirect, url_for, send_from_directory

from flask_cors import CORS

from blockchain import Blockchain


'''
from poa import username, password
'''
import sqlite3

from pyisemail import is_email



app = Flask(__name__)
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()



@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/configure')
def configure():
    return render_template('./configure.html')


@app.route('/entrada/new', methods=['POST'])
def new_entrada():
    entitat = request.form['confirmation_entitat']
    email=request.form['confirmation_email']
    usuari=request.form['confirmation_usuari']
    label=request.form['confirmation_label']
    info=request.form['confirmation_info']
    signature=request.form['signature']

    required = [entitat, email, usuari, label, info, signature]
    for elem in required:
        if elem=='':
            response = {'message': 'Falta informació'}
            return jsonify(response), 400

    # Create a new Transaction
    entrada_result = blockchain.submit_entrada(entitat, usuari, label, info, signature)

    if entrada_result == False:
        response = {'message': 'Entrada no vàlida!'}
        return jsonify(response), 406
    else:
        response = {'message': "Entrada vàlida: s'afegirà al CV (entrada #"+ str(entrada_result-1)+")"}
        return jsonify(response), 201


@app.route('/mine', methods=['GET'])
def mine():

    last_block = blockchain.previous_block
    previous_hash = blockchain.compute_hash(last_block)
    block = blockchain.new_block(previous_hash)

    response = {
        'message': "Nova Entrada realitzada",
        'index': block['index'],
        'entrades': block['entrades'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 201

@app.route('/unmine', methods=['POST'])
def unmine():
    entradaf=request.get_json()
    print(entradaf)
    entitat=entradaf[0]
    label=entradaf[1]
    info=entradaf[2]
    fora=blockchain.unsubmit_entrada(entitat, label, info)
    response={'entrada': 'eliminada'}
    return jsonify(response), 201


@app.route('/entrades/get', methods=['GET'])
def get_entrades():
    #Get entrada from entrada's pool
    entrades = blockchain.entrades
    response = {'entrades': entrades}
    return jsonify(response), 201


@app.route('/chain/get', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 201


@app.route('/view/cv', methods=['POST'])
def view_cv():
    email=request.form['email']
    if is_email(email):
        conn=sqlite3.connect('veuen.db')
        c=conn.cursor()
        c.execute("SELECT * FROM PodenVeure")
        nodes=c.fetchall()
        for i in range (len(nodes)):
            for elem in nodes[i]:
                if email in elem:
                    response = {'Resposta': 'Valida'}
                    conn.close()
                    return jsonify(response), 201
    else:
        response = {'Resposta': ' No valida'}
        return jsonify(response), 400

@app.route('/voyeur/list', methods=['GET'])
def is_already_allowed():
    conn=sqlite3.connect('veuen.db')
    c=conn.cursor()
    c.execute("SELECT * FROM PodenVeure")
    nodes=c.fetchall()
    lnodes=[]
    for elem in nodes:
        lnodes.append(elem)
    conn.close()
    response = {'nodes': lnodes}
    return jsonify(response), 201

@app.route('/node/voyeur', methods=['POST'])
def is_new_allowed():
    node = str(request.form['node'])

    '''
    nodes = str(values.get('nodes'))
    nodes.replace(" ", "").split(',')
    '''
    if is_email(node):
        conn=sqlite3.connect('veuen.db')
        c=conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS PodenVeure
                (node text
                )""")
        conn.commit()
        c.execute("SELECT * FROM PodenVeure")
        nodes=c.fetchall()
        lnodes=[]
        for elem in nodes:
            lnodes.append(elem)
            if elem[0]==node:
                return "Error: Node no vàlid", 400
        c.execute("INSERT INTO PodenVeure VALUES (?)", (node,))
        conn.commit()
        conn.close()
        lnodes.append(node)
        response = {'nodes': lnodes}
        return jsonify(response), 201

    else:
        return "Error: Node no vàlid", 400
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/logout')
def logout():
    shutdown_server()
    return render_template('./logout.html')

'''
if username=='Usuari_Exemple' and password=='tfg':
'''

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5001, type=int, help='port to listen to')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port, debug=True)
'''
else:
    print('POA NO SUPERAT')
'''

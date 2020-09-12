from collections import OrderedDict
import Crypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from uuid import uuid4
import hashlib
import binascii
from time import time
import json

class Blockchain:
    def __init__(self):
        self.entrades = []
        self.chain = []
        self.nodes = []
        self.create_genesis_block()

    def create_genesis_block(self):
        '''
        Creem el genesis block sense entrades amb un previous hash
        que es un str de 64 zeros (64 ja que
        es la longitud dels proxims hashes)
        '''
        h=''
        block = {
            'index': 0,
            'timestamp': time(),
            'entrades': [],
            'previous_hash': h.zfill(64),
        }
        self.entrades = []
        self.chain.append(block)
        return block

    def verify_signature(self, entitat, signature, entrada):
        '''
        Desenvolupament de criptografia asimetrica:
        Comprovem si la signatura correspon a l'entrada signada per
        la public key (normalment, ENTITAT tot i que
        podria ser el propi USUARI)
        '''
        public_key = RSA.importKey(binascii.unhexlify(entitat))
        verifier = PKCS1_v1_5.new(public_key)
        hash = SHA.new(str(entrada).encode('utf8'))
        try:
            verifier.verify(hash, binascii.unhexlify(signature))
            return True
        except ValueError:
            return False

        return verificacio

    def submit_entrada(self, entitat, usuari, label, info, signature):
        '''
        Per potencialment afegir una nova entrada
        '''
        entrada = OrderedDict({'entitat': entitat,
                                    'usuari': usuari,
                                    'label': label,
                                    'info': info})


        entrada_verification = self.verify_signature(entitat, signature, entrada)
        if entrada_verification:
            for clau in entrada:
                if clau == 'usuari':
                    del entrada['usuari']
                    self.entrades.append(entrada)
                    return len(self.chain)
        else:
            return False

    def unsubmit_entrada(self, entitat, label, info):
        '''
        En el cas que l'USUARI no vulgui afegir la potencial
        entrada al seu CV
        '''
        entradaf = OrderedDict({'entitat': entitat,
                                    'label':label,
                                    'info': info})
        self.entrades.remove(entradaf)

    def new_block(self, previous_hash):
        '''
        En el cas que l'USUARI si vulgui afegir l'entrada: creem
        el bloc
        '''
        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'entrades': self.entrades,
            'previous_hash': previous_hash,
        }
        self.chain.append(block)
        self.entrades = []
        return block

    def add_block(self, block):
        '''
        l'afegim a la cadena
        '''
        previous_hash = self.previous_block.hash
        self.chain.append(block)
        return block

    def is_public_key(self, puk):
        '''
        Comprovem que realment es tracti d'una puk (public key)
        '''
        if len(puk)==324 and puk.isalnum():
            return True
        else:
            return False

    @property
    def previous_block(self):
        return self.chain[-1]

    def compute_hash(self, block):
        '''
        Creem el hash (SHA-256) del bloc (encriptacio)
        Assegurem que el diccionari estigui ordenat per evitar
        errors
        '''
        block_string = json.dumps(block, sort_keys=True).encode('utf8')
        h=hashlib.new('sha256')
        h.update(block_string)
        return h.hexdigest()

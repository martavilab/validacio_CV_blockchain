import json
from urllib.parse import urlparse

from collections import OrderedDict

import Crypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

from uuid import uuid4

import hashlib

import binascii

from time import time




class Blockchain:
    def __init__(self):
        self.entrades = []
        self.chain = []
        self.nodes = []
        self.create_genesis_block()

    def create_genesis_block(self):

        block = {
            'index': 0,
            'timestamp': time(),
            'entrades': [],
            'previous_hash': 0000,
        }
        self.entrades = []
        self.chain.append(block)
        return block

    def verify_signature(self, entitat, signature, entrada):
        """
        Check that the provided signature corresponds to transaction
        signed by the public key (Entitat)
        """
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
        entradaf = OrderedDict({'entitat': entitat,
                                    'label':label,
                                    'info': info})
        self.entrades.remove(entradaf)

    def new_block(self, previous_hash):
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
        # IMPOSAR si l'usuari esta autentificat
        previous_hash = self.previous_block.hash
        self.chain.append(block)
        return block

    def is_public_key(self, puk):
        if len(puk)==324 and puk.isalnum():
            return True
        else:
            return False


    @property
    def previous_block(self):
        return self.chain[-1]


    def compute_hash(self, block):
        """
        Create a SHA-256 hash of a block
        """
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode('utf8')
        h=hashlib.new('sha256')
        h.update(block_string)

        return h.hexdigest()

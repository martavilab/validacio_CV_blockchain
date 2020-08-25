from collections import OrderedDict

import binascii
import flask
from flask import Flask, jsonify, request, render_template

import Crypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA



class Entrada:

    def __init__(self, entitat_public_key, entitat_private_key, usuari, info):
        self.entitat_public_key = entitat_public_key
        self.entitat_private_key = entitat_private_key
        self.usuari = usuari
        self.info = info

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
            return OrderedDict({'entitat_public_key': self.entitat_public_key,
                                'usuari': self.usuari,
                                'info': self.info})

    def sign_entrada(self):
        """
        Sign transaction with private key
        """
        private_key = RSA.importKey(binascii.unhexlify(self.entitat_private_key))
        signer = PKCS1_v1_5.new(private_key)
        hash = SHA.new(str(self.to_dict()).encode('utf8'))
        signature=binascii.hexlify(signer.sign(hash)).decode('ascii')
        return signature

#/usr/bin/python
# -*- coding: utf-8 -*-

import json
from bottle import Bottle, response, HTTPError, request, abort, auth_basic, parse_auth
from uuid import uuid4
from pymongo import Connection
from bson import json_util
from beaker.middleware import SessionMiddleware
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
import logging
from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib

logging.basicConfig(filename='data/logs/app.log',level=logging.DEBUG)

connection = Connection('localhost', 27017)
db = connection.mydatabase
app = Bottle()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 600,
    'session.auto': True,
    'session.data_dir': "cache",
}

engine = SessionMiddleware(app, session_opts)

SECRET_KEY = 'ffnnjeFpCtMd737NExBYhjodub3fpED2uZw03TNkhaA5cac3297f0d9f46e1gh3k83881ba0980215cd71e'
SECRET_AUTH_KEY = 'ffnnjeFpCtMd737NExBYhjodub3fpED2'

token_expiration = 31536000 # 365 J

BS = 32
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

def encrypt( raw , key):
    raw = pad(raw)
    iv = Random.new().read( AES.block_size )
    cipher = AES.new( key, AES.MODE_CBC, iv )
    return base64.b64encode( iv + cipher.encrypt( raw ) )

def decrypt( enc , key):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv )
    return unpad(cipher.decrypt( enc[16:] ))

def generate_auth_token(app_key, expiration = token_expiration):
    s = Serializer(SECRET_KEY, expires_in = expiration)
    return s.dumps({ 'id': app_key })

def verify_auth_token(auth_public_key, auth_protected_token):
    s = Serializer(SECRET_KEY)
    raw_protected_data = decrypt(auth_protected_token, SECRET_AUTH_KEY)
    try:
        token, private_key, public_key = raw_protected_data.split(':',2)
    except:
        return None
    entity = db['users'].find_one({'public_key': public_key, 'private_key': private_key})
    if not entity:
        return None
    if not (auth_public_key == entity['public_key']):
        return None
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    return True

def check_pass(username, password):
    auth = request.headers.get('Authorization')
    entity = None
    result = None
    if auth:
        username, password = parse_auth(auth)
    if not result:
        entity = db['users'].find_one({'username': username, 'password': password})
        if not entity:
            return False
    return True

def check_token(public_key, auth_token):
    auth = request.headers.get('Authorization')
    result = None
    if auth:
        public_key, auth_token = parse_auth_token(auth)
        try:
            result = verify_auth_token(auth_token, public_key)
            if not result:
                result = None
        except:
            result = None
    if not result:
        return False
    return True

def parse_auth_token(header):
    """ Parse HTTP authentication header string (ApiAuth) and return (token) or None"""
    try:
        method, data = header.split(None, 1)
        if method.lower() == 'apiauth':
            public_key, protected_token = data.split(':',1)
            return protected_token, public_key
    except (KeyError, ValueError):
        return None

def auth_token(check, realm="private", text="Access denied"):
    ''' Callback decorator to require HTTP auth (custom header)'''
    def decorator(func):
      def wrapper(*a, **ka):
        method, data = request.headers.get('Authorization').split(None, 1)
        #credential, token, autre = request.headers.get('Authorization') or (None, None)
        credential, token = data.split(':',1)
        if not check(credential, token):
          response.headers['WWW-Authenticate'] = 'ApiAuth realm="%s"' % realm
          return HTTPError(401, text)
        return func(*a, **ka)
      return wrapper
    return decorator
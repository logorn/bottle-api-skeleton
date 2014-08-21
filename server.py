#/usr/bin/python
# -*- coding: utf-8 -*-

import json
import bottle
from bottle import Bottle, request, redirect, response, HTTPError, route, run, request, abort, auth_basic, parse_auth
from uuid import uuid4
from pymongo import Connection
from bson import json_util
from beaker.middleware import SessionMiddleware
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
import logging
from Crypto import Random
from Crypto.Cipher import AES
import base64
import hashlib

logging.basicConfig(filename='cli-server.log',level=logging.DEBUG)
 
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

token_expiration = 120
token_expiration = 86400 # 24h
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

@app.route('/api/v1.0/documents', method='POST')
@auth_token(check_token)
def post_document():
    """
    CREATE DOCUMENT
    """
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        result = db['documents'].find_one({'_id':entity['_id']})
        if not result:
            db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@app.route('/api/v1.0/documents/:id', method='PUT')
@auth_token(check_token)
def put_document(id):
    """
    UPDATE DOCUMENT
    """
    entity = db['documents'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))
        
@app.route('/api/v1.0/documents', method='GET')
@auth_token(check_token)
def get_all_document():
    """
    RETRIEVE ALL DOCUMENTS
    """
    docs = db['documents'].find()
    if not docs:
        abort(404, 'No document found')
    response.content_type = "application/json"
    return json.dumps({'results':list(docs)},default=json_util.default)


@app.route('/api/v1.0/documents/:id', method='GET')
@auth_token(check_token)
def get_document(id):
    """
    RETRIEVE DOCUMENT
    """
    entity = db['documents'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity

@app.route('/api/v1.0/documents/:id', method='DELETE')
@auth_token(check_token)
def del_document(id):
    """
    DELETE DOCUMENT
    """
    entity = db['documents'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    entity = db['documents'].remove({'_id':id})
    return entity

@app.route('/api/v1.0/signup', method='POST')
def post_signup():
    """
    CREATE USER
    """
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entitypost = json.loads(data)
    result = db['users'].find_one({'username': entitypost['username'], 'password': entitypost['password']})
    if not result:
        entity = {
            '_id': uuid4().hex,
            'app_key' :  uuid4().hex,
            'private_key' : uuid4().hex,
            'public_key' : uuid4().hex,
            'username' : entitypost['username'],
            'password' : entitypost['password']
        }
        try:
            db['users'].save(entity)
        except ValidationError as ve:
            abort(400, str(ve))
    else:
        return {'status': 'OK'}

@app.route('/api/v1.0/login', method='POST')
def post_login():
    """
    LOGIN USER
    """
    data = request.body.readline()
    user_id = None
    if not data:
        abort(400, 'No data received')
    entitypost = json.loads(data)
    entity = db['users'].find_one({'username': entitypost['username'], 'password': entitypost['password']})
    if not entity:
        abort(404, 'No document with username = %s and password = %s' %  (entitypost['username'], entitypost['password']) )
    else:
        user_id = entity['_id']
    if user_id:
        response.status = 200
        return {'user_id': user_id}
    else:
        abort(401, 'Invalid username or password')

@app.route('/api/v1.0/token')
@auth_basic(check_pass)
def get_auth_token():
    auth = request.headers.get('Authorization')
    username, password = parse_auth(auth)
    entity = db['users'].find_one({'username': username, 'password': password})
    base_hash = hashlib.sha224(entity['app_key'] + entity['private_key']).hexdigest()
    token = generate_auth_token(hashlib.sha224(base_hash).hexdigest())
    protected_token = token.decode('ascii') + ':' + entity['private_key'] + ':' + entity['public_key']
    return { 'token': encrypt(protected_token, SECRET_AUTH_KEY) , 'public_key' : entity['public_key'] }

@app.route('/api/v1.0/basicauth', method='GET')
@auth_basic(check_pass)
def get_basic_auth():
    return {'status': 'OK'}

@app.route('/api/v1.0/session', method='GET')
def get_session():
    session= request.environ["beaker.session"]
    if "cpt" in session:
        session["cpt"]+=1
    else:
        session["cpt"]=1
    return "cpt:" + str(session["cpt"])
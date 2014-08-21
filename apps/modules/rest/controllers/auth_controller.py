# -*- coding: utf-8 -*-

from . import *

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
        db['users'].save(entity)
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

@app.route('/api/v1.0/demo', method='GET')
def get_demo():
    return {'status': 'OK'}
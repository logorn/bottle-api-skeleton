# -*- coding: utf-8 -*-

from . import *

class AuthController(object):

    @inject.param('service_user')
    def post_signup(self, service_user):
        """
        CREATE USER
        """
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entitypost = json.loads(data)

        result = service_user.Users.repository.find_one({'username': entitypost['username'], 'password': entitypost['password']})

        if not result:
            entity = {
                '_id': uuid4().hex,
                'app_key' :  uuid4().hex,
                'private_key' : uuid4().hex,
                'public_key' : uuid4().hex,
                'username' : entitypost['username'],
                'password' : entitypost['password']
            }
            service_user.Users.repository.save(entity)
        else:
            return {'status': 'OK'}

    @inject.param('service_user')
    def post_login(self, service_user):
        """
        LOGIN USER
        """
        data = request.body.readline()
        user_id = None
        if not data:
            abort(400, 'No data received')
        entitypost = json.loads(data)

        entity = service_user.Users.repository.find_one({'username': entitypost['username'], 'password': entitypost['password']})

        if not entity:
            abort(404, 'No document with username = %s and password = %s' %  (entitypost['username'], entitypost['password']) )
        else:
            user_id = entity['_id']
        if user_id:
            response.status = 200
            return {'user_id': user_id}
        else:
            abort(401, 'Invalid username or password')

    @auth_basic(check_pass)
    @inject.param('service_user')
    def get_auth_token(self, service_user):

        auth = request.headers.get('Authorization')
        username, password = parse_auth(auth)
        entity = service_user.Users.repository.find_one({'username': username, 'password': password})

        base_hash = hashlib.sha224(entity['app_key'] + entity['private_key']).hexdigest()
        token = generate_auth_token(hashlib.sha224(base_hash).hexdigest())
        protected_token = token.decode('ascii') + ':' + entity['private_key'] + ':' + entity['public_key']
        return { 'token': encrypt(protected_token, SECRET_AUTH_KEY) , 'public_key' : entity['public_key'] }

    @auth_basic(check_pass)
    def get_basic_auth(self):
        return {'status': 'OK'}

    def get_session(self):
        session= request.environ["beaker.session"]
        if "cpt" in session:
            session["cpt"]+=1
        else:
            session["cpt"]=1
        return "cpt:" + str(session["cpt"])
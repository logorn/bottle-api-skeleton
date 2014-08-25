# -*- coding: utf-8 -*-

from gevent import monkey
import sys
from . import *

monkey.patch_all()
monkey.patch_thread()

if 'threading' in sys.modules:
    del sys.modules['threading']

from apps.modules.rest.controllers.auth_controller import *
from apps.modules.rest.controllers.document_controller import *

class bootstrap:

    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._app = app
        self._route()
        self._engine = SessionMiddleware(self._app, session_opts)

    def _route(self):
        # auth controller class
        self._app.route('/api/v1.0/signup', method='POST', callback=AuthController().post_signup)
        self._app.route('/api/v1.0/login', method='POST', callback=AuthController().post_login)
        self._app.route('/api/v1.0/token', callback=AuthController().get_auth_token)
        self._app.route('/api/v1.0/basicauth', method='GET', callback=AuthController().get_basic_auth)
        self._app.route('/api/v1.0/session', method='GET', callback=AuthController().get_session)
        # document controller class
        self._app.route('/api/v1.0/documents', method='POST', callback=DocumentController().post_document)
        self._app.route('/api/v1.0/documents/:id', method='PUT', callback=DocumentController().put_document)
        self._app.route('/api/v1.0/documents', method='GET', callback=DocumentController().get_all_document)
        self._app.route('/api/v1.0/documents/:id', method='GET', callback=DocumentController().get_document)
        self._app.route('/api/v1.0/documents/:id', method='DELETE', callback=DocumentController().del_document)

    @app.error(404)
    def error404(self):
        return json.dumps({"error":"true", "message":"404 not found"}, default=json_util.default)

    def start(self):
        bottle.debug(True)
        bottle.run(app=self._engine, host=self._host, port=self._port, reloader=True, server='gevent')

    def main(self):
        """Run the command
        """

        host = self._host
        port = self._port

        server = bootstrap(host, port)
        server.start()
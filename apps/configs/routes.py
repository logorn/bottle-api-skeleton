
from apps.modules.rest.controllers.auth_controller import *
from apps.modules.rest.controllers.document_controller import *

class RoutesManager:
    def __init__(self, app):
        self._app = app

    def get_route(self):
        self.auth_controller()
        self.document_controller()
        return self._app

    def auth_controller(self):
        # auth controller class
        self._app.route('/api/v1.0/signup', method='POST', callback=AuthController().post_signup)
        self._app.route('/api/v1.0/login', method='POST', callback=AuthController().post_login)
        self._app.route('/api/v1.0/token', callback=AuthController().get_auth_token)
        self._app.route('/api/v1.0/basicauth', method='GET', callback=AuthController().get_basic_auth)
        self._app.route('/api/v1.0/session', method='GET', callback=AuthController().get_session)

    def document_controller(self):
        # document controller class
        self._app.route('/api/v1.0/documents', method='POST', callback=DocumentController().post_document)
        self._app.route('/api/v1.0/documents/:id', method='PUT', callback=DocumentController().put_document)
        self._app.route('/api/v1.0/documents', method='GET', callback=DocumentController().get_all_document)
        self._app.route('/api/v1.0/documents/:id', method='GET', callback=DocumentController().get_document)
        self._app.route('/api/v1.0/documents/:id', method='DELETE', callback=DocumentController().del_document)
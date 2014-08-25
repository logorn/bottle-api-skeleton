# -*- coding: utf-8 -*-

from gevent import monkey
import sys
from . import *

monkey.patch_all()
monkey.patch_thread()

if 'threading' in sys.modules:
    del sys.modules['threading']

class bootstrap:

    def __init__(self, host='localhost', port=8080):
        self._host = host
        self._port = port
        self._app = app
        self._route()
        self._engine = SessionMiddleware(self._app, session_opts)

    def _route(self):
        # routes manager
        from apps.configs.routes import RoutesManager
        self._app = RoutesManager(self._app).get_route()

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
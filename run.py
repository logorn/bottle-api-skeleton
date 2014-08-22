#/usr/bin/python
# -*- coding: utf-8 -*-

from apps.bootstrap import bootstrap

server = bootstrap(host='localhost', port=8080)
server.start()

#/usr/bin/python
# -*- coding: utf-8 -*-

import bottle
from gevent import monkey
monkey.patch_all()
from apps.bootstrap import engine


bottle.debug(True)

bottle.run(app=engine, host='0.0.0.0', port='8080', reloader=True, server='gevent')

# version sans utilisation de gevent
#bottle.run(app=engine, host='0.0.0.0', port='8080', reloader=True)

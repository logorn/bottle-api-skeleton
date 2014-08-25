# -*- coding: utf-8 -*-

from mongokit import Connection
from library.bas.entity.documents import Documents

conn = Connection()
conn.register([Documents])

class Documents(Documents):
    """"""
    def __init__(self):
        database = conn.mydatabase
        self.repository = database.documents
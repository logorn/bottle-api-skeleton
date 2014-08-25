# -*- coding: utf-8 -*-

from mongokit import Connection
from library.bas.entity.users import Users

conn = Connection()
conn.register([Users])

class Users(Users):
    """"""
    def __init__(self):
        database = conn.mydatabase
        self.repository = database.users
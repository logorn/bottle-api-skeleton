# -*- coding: utf-8 -*-

from mongokit import Document
import datetime

class Users(Document):
    __database__ = 'mydatabase'
    __collection__ = 'users'
    structure = {
        '_id': basestring,
        'username': basestring,
        'public_key': basestring,
        'private_key': basestring,
        'app_key': basestring,
        'password': basestring
    }
    required_fields = ['_id', 'username', 'public_key', 'private_key', 'app_key']
    use_dot_notation = True
    indexes = [
        {'fields': ['_id', 'public_key', 'private_key', 'app_key', 'password']},
    ]
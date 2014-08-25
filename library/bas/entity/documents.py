# -*- coding: utf-8 -*-

from mongokit import Document

class Documents(Document):
    __database__ = 'mydatabase'
    __collection__ = 'documents'
    structure = {
        '_id': basestring,
        'name': basestring,
    }
    required_fields = ['_id', 'name']
    use_dot_notation = True
    indexes = [
        {'fields': ['_id']},
    ]
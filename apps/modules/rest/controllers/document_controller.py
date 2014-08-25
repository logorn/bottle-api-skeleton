# -*- coding: utf-8 -*-

from . import *
from mongokit import Connection
from library.bas.entity.documents import Documents
conn = Connection()
conn.register([Documents])
database = conn.mydatabase
collection = database.documents

class DocumentController(object):

    @auth_token(check_token)
    def post_document(self):
        """
        CREATE DOCUMENT
        """
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entity = json.loads(data)
        if not entity.has_key('_id'):
            abort(400, 'No _id specified')

        result = collection.Documents.find_one({'_id':entity['_id']})
        if not result:
            collection.Documents.save(entity)

    @auth_token(check_token)
    def put_document(self, id):
        """
        UPDATE DOCUMENT
        """
        entity = collection.Documents.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entity = json.loads(data)
        if not entity.has_key('_id'):
            abort(400, 'No _id specified')
        collection.Documents.save(entity)

    @auth_token(check_token)
    def get_all_document(self):
        """
        RETRIEVE ALL DOCUMENTS
        """
        docs = collection.Documents.find()
        if not docs:
            abort(404, 'No document found')
        response.content_type = "application/json"
        return json.dumps({'results':list(docs)},default=json_util.default)

    @auth_token(check_token)
    def get_document(self, id):
        """
        RETRIEVE DOCUMENT
        """
        entity = collection.Documents.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        return entity

    @auth_token(check_token)
    def del_document(self, id):
        """
        DELETE DOCUMENT
        """
        entity = collection.Documents.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        entity = collection.Documents.remove({'_id':id})
        return entity
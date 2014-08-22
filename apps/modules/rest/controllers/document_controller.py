# -*- coding: utf-8 -*-

from . import *

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

        result = db['documents'].find_one({'_id':entity['_id']})
        if not result:
            db['documents'].save(entity)

    @auth_token(check_token)
    def put_document(self, id):
        """
        UPDATE DOCUMENT
        """
        entity = db['documents'].find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entity = json.loads(data)
        if not entity.has_key('_id'):
            abort(400, 'No _id specified')
        db['documents'].save(entity)

    @auth_token(check_token)
    def get_all_document(self):
        """
        RETRIEVE ALL DOCUMENTS
        """
        docs = db['documents'].find()
        if not docs:
            abort(404, 'No document found')
        response.content_type = "application/json"
        return json.dumps({'results':list(docs)},default=json_util.default)

    @auth_token(check_token)
    def get_document(self, id):
        """
        RETRIEVE DOCUMENT
        """
        entity = db['documents'].find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        return entity

    @auth_token(check_token)
    def del_document(self, id):
        """
        DELETE DOCUMENT
        """
        entity = db['documents'].find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        entity = db['documents'].remove({'_id':id})
        return entity
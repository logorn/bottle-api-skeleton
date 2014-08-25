# -*- coding: utf-8 -*-

from . import *

class DocumentController(object):

    @auth_token(check_token)
    @inject.param('service_document')
    def post_document(self, service_document):
        """
        CREATE DOCUMENT
        """
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entity = json.loads(data)
        if not entity.has_key('_id'):
            abort(400, 'No _id specified')

        result = service_document.Documents.repository.find_one({'_id':entity['_id']})

        if not result:
            service_document.Documents.repository.save(entity)

    @auth_token(check_token)
    @inject.param('service_document')
    def put_document(self, id, service_document):
        """
        UPDATE DOCUMENT
        """
        entity = service_document.Documents.repository.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        data = request.body.readline()
        if not data:
            abort(400, 'No data received')
        entity = json.loads(data)
        if not entity.has_key('_id'):
            abort(400, 'No _id specified')
        service_document.Documents.repository.save(entity)

    @auth_token(check_token)
    @inject.param('service_document')
    def get_all_document(self, service_document):
        """
        RETRIEVE ALL DOCUMENTS
        """
        docs = service_document.Documents.repository.find()
        if not docs:
            abort(404, 'No document found')
        response.content_type = "application/json"
        return json.dumps({'results':list(docs)},default=json_util.default)

    @auth_token(check_token)
    @inject.param('service_document')
    def get_document(self, id, service_document):
        """
        RETRIEVE DOCUMENT
        """
        entity = service_document.Documents.repository.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        return entity

    @auth_token(check_token)
    @inject.param('service_document')
    def del_document(self, id, service_document):
        """
        DELETE DOCUMENT
        """
        entity = service_document.Documents.repository.find_one({'_id':id})
        if not entity:
            abort(404, 'No document with id %s' % id)
        entity = service_document.Documents.repository.remove({'_id':id})
        return entity
import logging
from http import HTTPStatus
from flask import request
from flask_restx import Resource
from app.main.apis.v_01.controller import json_helper
from app.main.apis.v_01.model.city_model import CityModel as model
from app.main.service import city_service as service
from app.main.util.decorator import sign_in_required


API = model.namespace
ENTITY_NAME = "city"


@API.route('/')
class Entities(Resource):

    @API.doc(f'list_of_{ENTITY_NAME}s')
    @API.marshal_list_with(model.return_model)
    @sign_in_required
    def get(self):
        logging.info(f"Get {ENTITY_NAME} called")
        all_entities = service.get_all()
        logging.info(f"All {ENTITY_NAME}s list: {all_entities}")
        return all_entities, HTTPStatus.OK

    @API.doc(f'add_{ENTITY_NAME}')
    @API.expect(model.add_model, validate=True)
    @API.response(HTTPStatus.CREATED, 'Successfully added.')
    @sign_in_required
    def post(self):
        logging.info(f"Create {ENTITY_NAME} called")
        name_ua = json_helper.get_field(request, "name_ua")
        name_en = json_helper.get_field(request, "name_en")
        service.add(name_ua=name_ua, name_en=name_en)
        return HTTPStatus.CREATED


@API.route('/<int:id>')
@API.param('id')
@API.response(HTTPStatus.NOT_FOUND, 'Not found.')
class Entitiy(Resource):

    @API.doc(f'get_{ENTITY_NAME}')
    @API.marshal_with(model.return_model)
    @sign_in_required
    def get(self, id):
        logging.debug(f"Get {ENTITY_NAME} called. id: {id}")
        entity = service.get(id)
        logging.info(f"Got {ENTITY_NAME}: {entity}")
        return entity, HTTPStatus.OK

    @API.doc(f'update_{ENTITY_NAME}')
    @API.expect(model.update_model, validate=True)
    @sign_in_required
    def put(self, id):
        logging.debug(f"Update {ENTITY_NAME} called. id: {id}")
        name_ua = json_helper.get_field(request, "name_ua")
        name_en = json_helper.get_field(request, "name_en")
        service.update(id=id, name_ua=name_ua, name_en=name_en)
        return HTTPStatus.OK

    @API.doc(f'remove_{ENTITY_NAME}')
    @sign_in_required
    def delete(self, id):
        logging.debug(f"Delete {ENTITY_NAME} called. id: {id}")
        service.delete(id)
        return HTTPStatus.OK

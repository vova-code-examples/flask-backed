from http import HTTPStatus
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity
from app.main.apis.v_01.model.auth_model import AuthModel
from app.main.apis.v_01.controller import json_helper
from app.main.service import auth_service

API = AuthModel.auth_namespace


@API.route('/sign_up')
class SignUp(Resource):

    @API.doc('user sign up')
    @API.expect(AuthModel.sign_up_request, validate=True)
    @API.marshal_with(AuthModel.user_response)
    def post(self):
        username = json_helper.get_field(request, "username")
        password = json_helper.get_field(request, "password")
        auth_data = auth_service.sign_up(username=username, password=password)
        return auth_data, HTTPStatus.CREATED


@API.route('/sign_in')
class SignIn(Resource):

    @API.doc('user sign in')
    @API.expect(AuthModel.sign_in_request, validate=True)
    @API.marshal_with(AuthModel.user_response)
    def post(self):
        username = json_helper.get_field(request, "username")
        password = json_helper.get_field(request, "password")
        auth_data = auth_service.sign_in(username=username, password=password)
        return auth_data, HTTPStatus.OK


@API.route('/refresh_token')
class RefreshToken(Resource):

    @API.doc('refresh_token')
    @jwt_refresh_token_required
    @API.marshal_with(AuthModel.user_response)
    def get(self):
        user_id = get_jwt_identity()
        user = auth_service.refresh(user_id=user_id)
        return user, HTTPStatus.OK

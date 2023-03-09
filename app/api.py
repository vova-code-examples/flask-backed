from http import HTTPStatus
from flask_restx import Api
from flask import Blueprint
from app.main.exceptions.already_exist_exception import AlreadyExistException
from app.main.exceptions.not_found_exception import NotFoundException
from app.main.exceptions.unauthorized_exception import UnauthorizedException
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError
from app.main.apis.v_01.controller.auth_controller import API as auth_api
from app.main.apis.v_01.controller.city_controller import API as city_api



BLUEPRINT_V_01 = Blueprint('api_v_01', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
    }
}

API_V1 = Api(
    BLUEPRINT_V_01,
    title='Demo Backend',
    version="",
    security=['apikey'],
    authorizations=authorizations,
    validate=True,
    description='Demo Backend'
)

API_V1.add_namespace(auth_api, path='/auth')
API_V1.add_namespace(city_api, path='/city')


@API_V1.errorhandler
@API_V1.errorhandler(NotFoundException)
@API_V1.errorhandler(AlreadyExistException)
def handle_error(error):
    response_object = {
        'message': str(error),
    }
    print(error)
    return response_object, HTTPStatus.BAD_REQUEST


@API_V1.errorhandler(NoAuthorizationError)
@API_V1.errorhandler(ExpiredSignatureError)
@API_V1.errorhandler(UnauthorizedException)
def handle_auth_error(error):
    response_object = {
        'message': str(error),
    }
    return response_object, HTTPStatus.UNAUTHORIZED


def get_create_blueprint(env_name, version):
    API_V1.version = f"{version}-{env_name}"
    return BLUEPRINT_V_01

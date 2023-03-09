import traceback
import logging

from http import HTTPStatus
from time import strftime
from flask import request
from app.api import get_create_blueprint
from app.main import create_app
from app.main.config import CONFIG


APP = create_app(CONFIG)
BLUEPRINT_V_01 = get_create_blueprint(CONFIG.API_ENV, CONFIG.VERSION)
APP.register_blueprint(BLUEPRINT_V_01)
APP.app_context().push()


@APP.before_request
def before_request():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())


@APP.after_request
def after_request(response):
    ''' Logging after request processing '''
    # This avoids the duplication of registry in the log, since that 500 is already logged via @APP.errorhandler.
    if response.status_code < 500:
        time_string = strftime('[%Y-%b-%d %H:%M]')
        if response.status_code >= 400:
            logging.error('%s %s %s %s %s %s', time_string, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
        else:
            logging.info('%s %s %s %s %s %s', time_string, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
    response.headers.add('Access-Control-Allow-Origin', CONFIG.ACCESS_CONTROL_ALLOW_ORIGIN)
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,HEAD,POST,PUT,DELETE,PATCH,OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Headers, Origin, \
        Accept, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers, \
        X-Requested-With, Content-Range, Authorization, Client-Version')
    response.headers.add('Access-Control-Expose-Headers', 'Content-Range')
    return response


@APP.errorhandler(Exception)
def exceptions(exception):
    """ Logging after every Exception. """
    time_string = strftime('[%Y-%b-%d %H:%M]')
    trace_back = traceback.format_exc()
    logging.error('%s\n%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', exception, time_string, request.remote_addr, request.method, request.scheme, request.full_path, trace_back)
    return "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR

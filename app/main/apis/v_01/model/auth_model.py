from flask_restx import Namespace, fields


class AuthModel:
    auth_namespace = Namespace('auth')

    sign_in_request = auth_namespace.model('sign_in_request', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
    })

    sign_up_request = auth_namespace.model('sign_up_request', {
        'username': fields.String(required=True),
        'password': fields.String(required=True),
    })

    user_response = auth_namespace.model('user_response', {
        'access_token': fields.String(),
        'refresh_token': fields.String(),
    })

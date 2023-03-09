from functools import wraps
from flask import request
from app.main.exceptions.unauthorized_exception import UnauthorizedException
from app.main.util.auth import get_custom_auth_token_from_request, get_signed_in_user


def sign_in_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = get_custom_auth_token_from_request(request)
            user = get_signed_in_user(token)
            request.user_id = user.id
            request.user = user
        except UnauthorizedException as e:
            return {"errors": [e.message]}, 403
        return f(*args, **kwargs)
    return wrapper

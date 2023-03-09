import logging
import time
import jwt
import jwt.exceptions
from app.main.exceptions.unauthorized_exception import UnauthorizedException
from app.main.service import user_service
from app.main.config import CONFIG


def _generate_base_jwt_payload(id: int, expity_time):
    payload = {
        'iss': CONFIG.JWT_ISSUER,
        'sub': CONFIG.JWT_SUB,
        'aud': CONFIG.JWT_AUDIENCE,
        'iat': int(time.time()),
        'exp': int(time.time() + expity_time),
    }
    payload.update({'id': id})
    return payload


def _decode_custom_auth_token(token):
    try:
        return jwt.decode(
            token,
            CONFIG.AUTH_SECRET_KEY,
            audience=CONFIG.JWT_AUDIENCE,
            algorithms=CONFIG.JWT_ALGORITHM,
            options={'verify_exp': False}
        )
    except jwt.exceptions.ExpiredSignatureError:
        logging.info("Rejecting expired JWT login token")
        return None
    except Exception:
        logging.exception("Error decoding JWT login token")
        return None


def _get_user_id_from_custom_token(token):
    try:
        payload = _decode_custom_auth_token(token)
        # Don't check the expiry time of tokens for now
        if not payload or not payload['id']:
            return None
        return int(payload['id'])
    except Exception:
        logging.exception("Error getting user from decoded JWT token")


def get_custom_auth_token_from_request(request):
    auth_token = None
    if request.headers.get("Authorization", "").startswith("Bearer "):
        auth_token = request.headers["Authorization"][7:].strip()
    return auth_token


def generate_access_token(id):
    payload = _generate_base_jwt_payload(id=id, expity_time=CONFIG.ACCESS_EXPIRY_TIME)
    return jwt.encode(payload, CONFIG.AUTH_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM)


def generate_refresh_token(id):
    payload = _generate_base_jwt_payload(id=id, expity_time=CONFIG.REFRESH_EXPIRY_TIME)
    return jwt.encode(payload, CONFIG.AUTH_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM)


def get_signed_in_user(token):
    """Try to get the logged in user or throw"""
    if not token:
        raise UnauthorizedException("Errors.MISSING_TOKEN")
    id = _get_user_id_from_custom_token(token)
    if not id:
        raise UnauthorizedException("Errors.INVALID_TOKEN")

    user = user_service.get(id=id)
    if not user:
        raise UnauthorizedException("Errors.INVALID_TOKEN")
    return user

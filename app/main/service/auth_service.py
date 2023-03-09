import logging
from app.main.service import user_service
from app.main.util.auth import generate_access_token, generate_refresh_token
from app.main.exceptions.unauthorized_exception import UnauthorizedException
from app.main.exceptions.already_exist_exception import AlreadyExistException


def sign_in(username: str, password: str):
    user = user_service.get_by_username(username=username)
    if not user or not user.check_password(password):
        raise UnauthorizedException("Incorrect credentials")
    result_data = _get_user_data(user=user)
    return result_data


def sign_up(username: str, password: str):
    user = user_service.get_by_username(username=username)
    if user:
        raise AlreadyExistException(f"user with username {username} already exists")
    user = user_service.add(username=username, password=password)
    result_data = _get_user_data(user=user)
    return result_data


def refresh(user_id: int):
    user = user_service.get(id=user_id)
    if not user:
        logging.error(f"Wrong user id: {user_id}")
        raise UnauthorizedException()
    result_data = user._get_user_data(user=user)
    return result_data


def _get_user_data(user):
    result_data = {
        'id': user.id,
        'username': user.username,
        'access_token': generate_access_token(id=user.id),
        'refresh_token': generate_refresh_token(id=user.id)
    }
    return result_data

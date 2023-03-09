import logging
from app.main import DB, FLASK_BCRYPT
from app.main.db_entities.user import User as DB_Entity
from app.main.exceptions.not_found_exception import NotFoundException


entity_name = "user"


def get_all():
    logging.info(f"get all {entity_name}s called")
    return DB_Entity.query.all()


def delete(id: int):
    logging.info(f"delete {entity_name} called. {entity_name} id: {id}")
    entity = DB_Entity.query.filter_by(id=id).first()
    if not entity:
        raise NotFoundException()
    DB.session.delete(entity)
    DB.session.commit()
    logging.info(f"{entity_name} with id {id} deleted")
    return True


def get(id: int):
    logging.info(f"get {entity_name} called. id: {id}")
    entity = DB_Entity.query.filter_by(id=id).first()
    if not entity:
        raise NotFoundException()
    logging.info(f"found {entity_name}: {entity}")
    return entity


def get_by_username(username: str):
    logging.info(f"get {entity_name} by username called. username: {username}")
    entity = DB_Entity.query.filter_by(username=username).first()

    logging.info(f"found {entity_name} {entity}")
    return entity


def add(username: str, password: str):
    logging.info(f"add {entity_name} called.")
    password_hash = FLASK_BCRYPT.generate_password_hash(password).decode('utf-8')
    new_entity = DB_Entity(username=username, password_hash=password_hash)
    DB.session.add(new_entity)
    DB.session.commit()
    logging.info(f"{entity_name} is added to db {new_entity}")
    return new_entity


def update(id: int, nickname: str, email: str, pin: str):
    logging.info(f"update {entity_name} called. id: {id}")
    entity = DB_Entity.query.filter_by(id=id).one_or_none()
    if not entity:
        raise NotFoundException()
    entity.nickname = nickname
    entity.email = email.strip().lower() if email else None
    entity.pin = pin
    DB.session.commit()
    logging.info(f"{entity_name} is updated {entity}")
    return entity

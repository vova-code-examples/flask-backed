import logging
from app.main import DB
from app.main.db_entities.city import City as DB_Entity
from app.main.exceptions.not_found_exception import NotFoundException


entity_name = "city"


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
    logging.info(f"found {entity_name} {entity}")
    return entity


def get_by_name(name: str):
    logging.info(f"get {entity_name} by name called. name: {name}")
    entity = DB_Entity.query.filter_by(name_ua=name).first()
    if not entity:
        entity = DB_Entity.query.filter_by(name_en=name).first()
    logging.info(f"found {entity_name} {entity}")
    return entity


def add(name_ua: str, name_en: str):
    logging.info(f"add {entity_name} called. name_ua: {name_ua}, name_en: {name_en}")
    new_entity = DB_Entity(name_ua=name_ua, name_en=name_en)
    DB.session.add(new_entity)
    DB.session.commit()
    logging.info(f"{entity_name} is added to db {new_entity}")
    return new_entity


def update(id: int, name_ua: str, name_en: str):
    logging.info(f"update {entity_name} called. id: {id}, name_ua: {name_ua}, name_en: {name_en}")
    entity = DB_Entity.query.filter_by(id=id).one_or_none()
    if not entity:
        raise NotFoundException()
    if name_ua is not None:
        entity.name_ua = name_ua
    if name_en is not None:
        entity.name_en = name_en
    DB.session.commit()
    logging.info(f"{entity_name} is updated {entity}")
    return entity

import logging
from app.main import DB
from flask_migrate import upgrade
from app.main.db_utils.seed import create_mandatory_info
from sqlalchemy_utils.functions import database_exists, create_database


def check_db():
    logging.info("Checking DB existance")
    if not database_exists(DB.get_engine().url):
        logging.info("DB is not created. Creating empty DB")
        create_database(DB.get_engine().url)

    logging.info("Run upgrade migrations")
    upgrade()
    logging.warning("Creating mandatory info")
    create_mandatory_info()

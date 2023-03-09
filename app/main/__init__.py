''' Application main module '''
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
DB = SQLAlchemy(metadata=metadata)
DB_BASE = declarative_base()

MIGRATE = Migrate()
FLASK_BCRYPT = Bcrypt()
JWTMANAGER = JWTManager()
OAUTH = OAuth()


def create_app(config):
    FORMAT = '%(asctime)s : %(levelname)s : %(processName)s : %(name)s : %(funcName)s : %(message)s'
    logging.basicConfig(level=config.LOGGING_LEVEL, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    logging.info(f"Logging set up. Level: {config.LOGGING_LEVEL}")
    logger.setLevel(config.LOGGING_LEVEL)

    logging.info("Initializing app")
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config)

    logging.info(f"Initializing DB. DB_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    DB.init_app(app)
    MIGRATE.init_app(app, DB, render_as_batch=True)
    FLASK_BCRYPT.init_app(app)
    JWTMANAGER.init_app(app)
    OAUTH.init_app(app)
    return app

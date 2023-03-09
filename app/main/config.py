import os
import json
import logging
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    LOGGING_LEVEL = logging.DEBUG
    API_ENV = os.getenv('API_ENV')
    ACCESS_CONTROL_ALLOW_ORIGIN = '*'
    VERSION = "unknown"

    PORT = os.getenv('FLASK_RUN_PORT')
    HOST = os.getenv('FLASK_RUN_HOST')

    JWT_ALGORITHM = 'HS256'
    AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
    JWT_AUDIENCE = "https://demo_backend.com.ua"
    JWT_ISSUER = "auth@demo_backend.com.ua"
    JWT_SUB = "auth@demo_backend.com.ua"
    ACCESS_EXPIRY_TIME = 60 * 60 * 24  # 1 day
    REFRESH_EXPIRY_TIME = 60 * 60 * 24 * 30  # 1 month


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    DEBUG = True
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(BaseConfig):
    ''' Production configuration class '''
    DEBUG = False
    LOGGING_LEVEL = logging.WARNING

    # DB_INSTANCE_IP = os.getenv('DB_INSTANCE_IP')
    # DB_USERNAME = os.getenv('DB_USERNAME')
    # DB_USER_PASSWORD = os.getenv('DB_USER_PASSWORD')
    # DB_NAME = os.getenv('DB_NAME')
    # DB_PORT = os.getenv('DB_PORT')
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_USER_PASSWORD}@{DB_INSTANCE_IP}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'prod.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
env_name = os.getenv('API_ENV') or 'dev'
CONFIG = config_by_name[env_name]

packaje_json_file = open('./package.json')
packaje_json = json.load(packaje_json_file)
CONFIG.VERSION = f"{packaje_json['version']}"

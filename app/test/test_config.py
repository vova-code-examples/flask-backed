import os
import unittest
from flask import current_app
from flask_testing import TestCase
from manage import APP
from app.main.config import BASE_DIR


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        APP.config.from_object('app.main.config.DevelopmentConfig')
        return APP

    def test_app_is_development(self):
        self.assertTrue(APP.config['DEBUG'])
        self.assertFalse(current_app is None)
        self.assertEqual(APP.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'dev.db'))


class TestTestingConfig(TestCase):
    def create_app(self):
        APP.config.from_object('app.main.config.TestingConfig')
        return APP

    def test_app_is_testing(self):
        self.assertTrue(APP.config['DEBUG'])
        self.assertEqual(APP.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'test.db'))


class TestProductionConfig(TestCase):
    def create_app(self):
        APP.config.from_object('app.main.config.ProductionConfig')
        return APP

    def test_app_is_production(self):
        self.assertFalse(APP.config['DEBUG'])
        self.assertEqual(APP.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///' + os.path.join(BASE_DIR, 'db', 'prod.db'))


if __name__ == '__main__':
    unittest.main()

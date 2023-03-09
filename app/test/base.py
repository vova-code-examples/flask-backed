''' Base test class '''
from flask_testing import TestCase

from app.main import DB
from manage import APP


class BaseTestCase(TestCase):
    ''' Base Tests '''

    def create_app(self):
        APP.config.from_object('app.main.config.TestingConfig')
        return APP

    def setUp(self):
        DB.create_all()
        DB.session.commit()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()

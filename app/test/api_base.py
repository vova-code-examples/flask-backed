''' Base test class '''
import datetime
import json

from app.main import DB
from app.main.db_entities.user import User
from app.test.base import BaseTestCase


class APIBaseTestCase(BaseTestCase):
    ''' API Base Tests '''

    def setUp(self):
        ''' login before testing API '''
        super().setUp()
        user = User(
            username='admin',
            password='@dm1n',
        )
        DB.session.add(user)
        DB.session.commit()
        with self.client:
            self.client.post(
                '/auth/token',
                data=json.dumps(dict(
                    email='admin',
                    password='@dm1n'
                )),
                content_type='application/json'
            )

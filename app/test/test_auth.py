''' Auth tests '''
import json
import unittest
from http import HTTPStatus
from app.test.base import BaseTestCase


class TestAuthBlueprint(BaseTestCase):
    ''' Auth endpoint to manipulate JWT tokens '''

    def test_sign_up(self):
        """ Test for user registration """
        with self.client:
            response = sign_up_user(self)
            data = json.loads(response.data.decode())
            self.assertIsNotNone(data['access_token'])
            self.assertIsNotNone(data['refresh_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        username = "some_username"
        sign_up_user(self, username=username)
        with self.client:
            response = sign_up_user(self, username=username)
            data = json.loads(response.data.decode())
            self.assertEqual(data['message'], f'user with username {username} already exists')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            response = sign_up_user(self)
            data = json.loads(response.data.decode())
            self.assertIsNotNone(data['access_token'])
            self.assertIsNotNone(data['refresh_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, HTTPStatus.CREATED)
            
            # registered user login
            response = sign_in_user(self)
            data = json.loads(response.data.decode())
            self.assertIsNotNone(data['access_token'])
            self.assertIsNotNone(data['refresh_token'])
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = sign_in_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'Incorrect credentials')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


def sign_up_user(self, username="username", password="123456"):
    data = json.dumps(dict(username=username, password=password))
    return self.client.post('/auth/sign_up', data=data, content_type='application/json')


def sign_in_user(self, username="username", password="123456"):
    data = json.dumps(dict(username=username, password=password))
    return self.client.post('/auth/sign_in', data=data, content_type='application/json')


if __name__ == '__main__':
    unittest.main()

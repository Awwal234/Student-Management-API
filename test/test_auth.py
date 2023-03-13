import unittest
from runserver import app
import json


class SignupTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_signup(self):
        data = {
            'name': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        }
        response = self.client.post(
            '/api/auth/signup', data=json.dumps(data), content_type='application/json')
        print(json.loads(response.text))
        self.assertEqual(response.status_code, 201)

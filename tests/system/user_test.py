from models.user import UserModel
from tests.not_unit_base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        # client pretends to be client to send api requests (GET, POST, PUT/PATCH, DELETE)
        with self.app() as client:
            # Allows test database to be built
            with self.app_context():
                # Being sent as Form Data
                response = client.post('/register', json={'username': 'Test User', 'password': 'Test Password'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('Test User'))
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'User created successfully'})

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'Test User', 'password': 'Test Password'})
                auth_response = client.post('/auth',
                                            json={'username': 'Test User', 'password': 'Test Password'},
                                            headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())  # [access_token]


    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', json={'username': 'Test User', 'password': 'Test Password'})
                response = client.post('/register', json={'username': 'Test User', 'password': 'Test Password'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'A user with that username already exists'})

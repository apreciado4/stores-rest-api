import json

from models.item import ItemModel
from models.user import UserModel
from tests.not_unit_base_test import BaseTest


class TestItem(BaseTest):
    def setUp(self):
        super(TestItem, self).setUp()
        with self.app() as client:
            with self.app_context():
                # client.post('/register', data={'username': 'Test User', 'password': 'Test Password'})
                UserModel("Test User", "Test Password").save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'Test User', 'password': 'Test Password'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_response.data)['access_token']
                self.header = {'Authorization': f'JWT {auth_token}'}

    def test_add_item(self):
        with self.app() as client:
            with self.app_context():
                # client.post('store/Test_Store', data={'name': 'Test_Store'})
                UserModel("Test User", "Test Password").save_to_db()

                response = client.post('item/Test',
                                       data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test', 'price': 20.0})

    def test_add_item_duplicate(self):
        with self.app() as client:
            with self.app_context():
                # client.post('store/Test_Store', data={'name': 'Test_Store'})
                UserModel("Test User", "Test Password").save_to_db()

                client.post('item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})
                response = client.post('item/Test',
                                       data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                                       headers={'Content-Type': 'application/json'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "An item with name 'Test' already exists."})

    def test_find_item(self):
        with self.app() as client:
            with self.app_context():
                #         client.post('/register', data={'username': 'Test User', 'password': 'Test Password'})
                #         # UserModel("Test User", "Test Password").save_to_db()
                #         auth_response = client.post('/auth',
                #                                     data=json.dumps({'username': 'Test User', 'password': 'Test Password'}),
                #                                     headers={'Content-Type': 'application/json'})
                #
                #         auth_token = json.loads(auth_response.data)['access_token']
                #         header = {'Authorization': f'JWT {auth_token}'}

                client.post('/store/Test_Store', data={'name': 'Test_Store'})
                client.post('item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})

                response = client.get('/item/Test', headers=self.header)

                self.assertNotEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test', 'price': 20.0})

    def test_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'Test User', 'password': 'Test Password'})
                # UserModel("Test User", "Test Password").save_to_db()
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'Test User', 'password': 'Test Password'}),
                                            headers={'Content-Type': 'application/json'})

                auth_token = json.loads(auth_response.data)['access_token']
                header = {'Authorization': f'JWT {auth_token}'}

                response = client.get('/item/Test', headers=header)

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Item not found'})

    def test_find_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/Test')

                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Could not authorize. Did you include a valid Authorization Header'})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test_Store', data={'name': 'Test_Store'})
                client.post('/item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})

                response = client.delete('/item/Test', data={'name': 'Test'})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Item deleted'})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                response = client.put('item/Test',
                                      data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                                      headers={'Content-Type': 'application/json'})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test', 'price': 20.0})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                client.put('item/Test',
                           data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                           headers={'Content-Type': 'application/json'})

                response = client.put('item/Test',
                                      data=json.dumps({'name': 'Test', 'price': 15, 'store_id': 1}),
                                      headers={'Content-Type': 'application/json'})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('Test').price, 15.0)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test', 'price': 15.0})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                client.post('item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})
                response = client.get('/items')

                self.assertDictEqual({'items': [{'id': 1, 'name': 'Test', 'price': 20}]},
                                     json.loads(response.data))

    def test_item_empty_list(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/items')

                self.assertDictEqual({'items': []},
                                     json.loads(response.data))

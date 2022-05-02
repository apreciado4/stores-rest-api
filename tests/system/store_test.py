from models.store import StoreModel
from tests.not_unit_base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('store/Test_Store', data={'name': 'Test_Store'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('Test_Store'))
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test_Store', 'items': []})

    def test_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                response = client.post('store/Test_Store', data={'name': 'Test_Store'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A store with name 'Test_Store' already exists."})

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                response = client.get('store/Test_Store', data={'name': 'Test_Store'})

                self.assertIs(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test_Store', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('store/Test_Store', data={'name': 'Test_Store'})

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Store not found'})

    def test_store_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                client.post('item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})

                response = client.get('store/Test_Store', data={'name': 'Test_Store'})

                self.assertIsNot(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'Test_Store', 'items': [{
                                         'id': 1,
                                         'name': 'Test',
                                         'price': 20.0
                                     }]})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('store/Test_Store', data={'name': 'Test_Store'})
                self.assertIsNotNone(StoreModel.find_by_name('Test_Store'))

                response = client.delete('store/Test_Store', data={'name': 'Test_Store'})

                self.assertDictEqual(json.loads(response.data),
                                     {'message': 'Store deleted'})
                self.assertIsNone(StoreModel.find_by_name('Test_Store'))

    def test_get_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test_Store', data={'name': 'Test_Store'})
                response = client.get('/stores')

                # self.assertEqual(response.status_code, 201)

                self.assertIsNotNone(response.data)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'id': 1, 'items': [], 'name': 'Test_Store'}]})

    def test_get_store_list_with_item(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/Test_Store', data={'name': 'Test_Store'})
                client.post('item/Test',
                            data=json.dumps({'name': 'Test', 'price': 20, 'store_id': 1}),
                            headers={'Content-Type': 'application/json'})

                response = client.get('/stores')

                self.assertIsNot(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'id': 1, 'name': 'Test_Store',
                                                  'items':
                                                      [{'id': 1, 'name': 'Test', 'price': 20.0}]}]})

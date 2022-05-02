from models.store import StoreModel
from models.item import ItemModel
from tests.not_unit_base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("Test Store")

        self.assertListEqual(store.items.all(), [],
                             "The stores items length was not 0 though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store")

            self.assertIsNone(StoreModel.find_by_name("Test Store"),
                              "StoreModel query returned store though nothing was written in database.")

            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name("Test Store"),
                                 "StoreModel query did not return store though store should have been written into db.")

            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name("Test Store"),
                              "StoreModel query returned store though store should have been deleted from db.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test", 20, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1, "The Store Items List should have length of 1")
            self.assertEqual(store.items.first().name, "Test", "First store item name should be 'Test'")

    def test_store_json(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test", 20, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {"id": 1, "name": "Test Store", "items": [{'id': 1, "name": "Test", "price": 20.0}]}

            self.assertDictEqual(expected, store.json(),
                                 "Store json incorrect name should be 'Test Store' and items should have Item json")


from models.user import UserModel
from tests.not_unit_base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('Test User', 'Test Password')

            self.assertIsNone(UserModel.find_by_username('Test User'),
                              f'Query returned object with name {user.username}, though nothing has been written into database.')
            self.assertIsNone(UserModel.find_by_id(1),
                              f'Query returned object with id 1, though nothing has been written into database.')

            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_username("Test User"),
                                 'Query returned None though object user should be found.')
            self.assertIsNotNone(UserModel.find_by_id(1),
                                 'Query returned None though object user should be found.')


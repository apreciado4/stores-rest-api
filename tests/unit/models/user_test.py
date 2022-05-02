from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('Test User', 'Test Password')

        self.assertEqual(user.username, 'Test User',
                         'user.username does not equal what is expected, username should be "Test User"')
        self.assertEqual(user.password, 'Test Password',
                         'user.password does not equal what is expected, password should be "Test Password"')


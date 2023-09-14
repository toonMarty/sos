import unittest
from app.models.user import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        """
        Test that password exists and is hashed
        """
        u = User(password='nice try')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        """
        Test that the password attribute cannot
        be read
        """
        u = User(password='nice try')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='nice try')
        self.assertTrue(u.check_password('nice try'))
        self.assertFalse(u.check_password('not nice try'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

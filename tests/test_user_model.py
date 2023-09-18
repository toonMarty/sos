import time
import unittest
from app.models.user import User
from app import db, create_app


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

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

    def test_valid_confirmation_token(self):
        u = User(first_name='test', last_name='testing', username='test',
                 email='test@test.com',
                 department='testing', password='nice try')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u1 = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')

        u2 = User(first_name='test2', last_name='testing2', username='test2',
                  email='test2@test.com', department='testing',
                  password='not nice try')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        u = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')

        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(15)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        u = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(User.reset_password(token, 'dog'))
        self.assertTrue(u.check_password('dog'))

    def test_invalid_reset_token(self):
        u = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertFalse(User.reset_password(token + 'cow', 'shed'))
        self.assertTrue(u.check_password('nice try'))

    def test_valid_email_change_token(self):
        u = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')
        db.session.add(u)
        db.session.commit()
        token = u.generate_email_change_token('johnnytest@example.com')
        self.assertTrue(u.change_email(token))
        self.assertTrue(u.email == 'johnnytest@example.com')

    def test_invalid_email_change_token(self):
        u1 = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')

        u2 = User(first_name='test2', last_name='testing2', username='test2',
                  email='test2@test.com', department='testing',
                  password='not nice try')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        token = u1.generate_email_change_token('johnnytest@testing.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'test2@test.com')

    def test_duplicate_email_token(self):
        u1 = User(first_name='test', last_name='testing', username='test',
                  email='test@test.com', department='testing',
                  password='nice try')

        u2 = User(first_name='test2', last_name='testing2', username='test2',
                  email='test2@test.com', department='testing',
                  password='not nice try')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        token = u1.generate_email_change_token('test@test.com')
        self.assertFalse(u2.change_email(token))
        self.assertTrue(u2.email == 'test2@test.com')






from hashlib import pbkdf2_hmac
from unittest import TestCase

from sqli.dao.user import User


class UserDAOTests(TestCase):
    def test_password_verify(self):
        salt = bytes.fromhex('00112233445566778899aabbccddeeff')
        digest = pbkdf2_hmac('sha256', b'correct', salt, 200000).hex()
        encoded = 'pbkdf2_sha256$200000${}${}'.format(salt.hex(), digest)
        user = User(1, 'Test', None, 'Student', 'student', encoded, False)
        self.assertTrue(user.check_password('correct'))
        self.assertFalse(user.check_password('wrong'))

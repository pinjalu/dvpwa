from hashlib import md5, pbkdf2_hmac
from unittest import TestCase

from sqli.dao.user import User


class UserDAOTests(TestCase):
    def test_password_legacy_digest_rejected(self):
        legacy_digest = md5(b'correct').hexdigest()
        user = User(1, 'Test', None, 'Student', 'student', legacy_digest, False)
        self.assertFalse(user.check_password('correct'))

    def test_password_verify(self):
        salt = bytes.fromhex('00112233445566778899aabbccddeeff')
        digest = pbkdf2_hmac('sha256', b'correct', salt, 200000).hex()
        encoded = 'pbkdf2_sha256$200000${}${}'.format(salt.hex(), digest)
        user = User(1, 'Test', None, 'Student', 'student', encoded, False)
        self.assertTrue(user.check_password('correct'))
        self.assertFalse(user.check_password('wrong'))

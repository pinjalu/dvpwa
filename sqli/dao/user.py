from hashlib import pbkdf2_hmac
from hmac import compare_digest
from secrets import token_hex
from typing import NamedTuple, Optional

from aiopg import Connection


class User(NamedTuple):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    username: str
    pwd_hash: str
    is_admin: bool

    @classmethod
    def from_raw(cls, raw: tuple):
        return cls(*raw) if raw else None

    @staticmethod
    async def get(conn: Connection, id_: int):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, first_name, middle_name, last_name, '
                'username, pwd_hash, is_admin FROM users WHERE id = %s',
                (id_,),
            )
            return User.from_raw(await cur.fetchone())

    @staticmethod
    async def get_by_username(conn: Connection, username: str):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, first_name, middle_name, last_name, '
                'username, pwd_hash, is_admin FROM users WHERE username = %s',
                (username,),
            )
            return User.from_raw(await cur.fetchone())

    @staticmethod
    def hash_password(password: str):
        salt = token_hex(16)
        rounds = 200000
        digest = pbkdf2_hmac('sha256', password.encode('utf-8'),
                             bytes.fromhex(salt), rounds).hex()
        return 'pbkdf2_sha256${}${}${}'.format(rounds, salt, digest)

    @staticmethod
    async def set_password(conn: Connection, id_: int, password: str):
        async with conn.cursor() as cur:
            await cur.execute('UPDATE users SET pwd_hash = %s WHERE id = %s',
                              (User.hash_password(password), id_))

    def check_password(self, password: str):
        try:
            scheme, rounds, salt, expected = self.pwd_hash.split('$')
            if scheme != 'pbkdf2_sha256' or int(rounds) < 100000:
                return False
            actual = pbkdf2_hmac('sha256', password.encode('utf-8'),
                                 bytes.fromhex(salt), int(rounds)).hex()
            return compare_digest(actual, expected)
        except (ValueError, TypeError):
            return False

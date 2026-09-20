"""In-memory transports for real DAO queries and aiohttp route handlers."""
from contextlib import AbstractAsyncContextManager
from datetime import datetime
from hashlib import md5
import re
import sqlite3
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

import aioredis
from aiohttp import CookieJar, web
from aiohttp.test_utils import TestClient, TestServer, make_mocked_request
from aiohttp_session import SESSION_KEY
from aiohttp_session.redis_storage import RedisStorage

from sqli import app as application
from sqli.dao.user import User
from sqli.services.redis import encode_session, decode_session
from sqli.utils.auth import session_cookie_settings
from sqli.utils.jinja2 import csrf_processor


class Cursor(AbstractAsyncContextManager):
    def __init__(self, database):
        self.cursor = database.cursor()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        self.cursor.close()

    async def execute(self, query, params=()):
        # Translate driver placeholders only; SQLite executes the SQL itself.
        query = re.sub(r'%\((\w+)\)s', r':\1', query)
        query = query.replace('%s', '?').replace('%%', '%')
        self.cursor.execute(query, params)

    async def fetchone(self):
        return self.cursor.fetchone()

    async def fetchall(self):
        return self.cursor.fetchall()


class Database(AbstractAsyncContextManager):
    def __init__(self):
        sqlite3.register_converter('timestamp', lambda value: datetime.fromisoformat(value.decode()))
        self.raw = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        self.raw.executescript('''
            CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT);
            CREATE TABLE users (id INTEGER PRIMARY KEY, first_name TEXT,
                middle_name TEXT, last_name TEXT, username TEXT, pwd_hash TEXT,
                is_admin BOOLEAN);
            CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT, description TEXT);
            CREATE TABLE course_reviews (id INTEGER PRIMARY KEY,
                date timestamp DEFAULT CURRENT_TIMESTAMP, course_id INTEGER, review_text TEXT);
            CREATE TABLE enrolments (user_id INTEGER, course_id INTEGER);
            INSERT INTO students VALUES (1, 'Alice'), (2, 'Bob');
            INSERT INTO courses VALUES (1, 'Math', 'Course one'), (2, 'Physics', 'Course two');
            INSERT INTO enrolments VALUES (1, 1);
        ''')

    def cursor(self):
        return Cursor(self.raw)

    def acquire(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        pass


class MemoryRedis(aioredis.commands.Redis):
    def __init__(self):
        self.values = {}

    def __await__(self):
        async def acquire():
            return self
        return acquire().__await__()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        pass

    async def get(self, key):
        return self.values.get(key)

    async def set(self, key, value, expire=0):
        self.values[key] = value.encode('utf-8') if isinstance(value, str) else value


class ViewCase(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.db = Database()
        # A valid account on either the baseline or salted-password branches.
        digest = (User.hash_password('correct') if hasattr(User, 'hash_password')
                  else md5(b'correct').hexdigest())
        self.db.raw.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (1, 'Test', None, 'Student', 'student', digest, False))
        with patch.object(application, 'setup_database'), patch.object(application, 'setup_redis'):
            app = application.init([])
        app['db'] = self.db
        app['redis'] = MemoryRedis()
        self.app = app
        server = TestServer(app)
        await server.start_server()
        # Permit Secure cookies over the loopback test transport without changing app settings.
        jar = CookieJar(unsafe=True, treat_as_secure_origin=[server.make_url('/')])
        self.client = TestClient(server, cookie_jar=jar)
        await self.client.start_server()

    async def asyncTearDown(self):
        await self.client.close()
        self.db.raw.close()

    async def login(self, password='correct'):
        return await self.client.post('/', data={'username': 'student', 'password': password})

    async def review_token(self):
        cookies = self.client.session.cookie_jar.filter_cookies(self.client.make_url('/'))
        request = make_mocked_request('GET', '/courses/1/review', app=self.app,
                                     headers={'Cookie': cookies.output(header='', sep=';').strip()})
        storage = RedisStorage(self.app['redis'], encoder=encode_session,
                               decoder=decode_session, **session_cookie_settings(self.app))
        request[SESSION_KEY] = await storage.load_session(request)
        context = await csrf_processor(request)
        token = context['csrf_token']()
        await storage.save_session(request, web.Response(), request[SESSION_KEY])
        return token

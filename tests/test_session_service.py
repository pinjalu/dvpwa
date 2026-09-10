from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from aiohttp import web
from aiohttp.test_utils import make_mocked_request
from aiohttp_session import Session
from aiohttp_session.redis_storage import RedisStorage

from sqli.services.redis import decode_session, encode_session
from tests.support import MemoryRedis


class SessionServiceTests(IsolatedAsyncioTestCase):
    async def test_session_expiry(self):
        storage = RedisStorage(MemoryRedis(), max_age=60,
                               encoder=encode_session, decoder=decode_session)
        with patch('aiohttp_session.time.time', return_value=1000000):
            session = Session(None, data=None, new=True, max_age=60)
            session['user_id'] = 1
            response = web.Response()
            await storage.save_session(make_mocked_request('GET', '/'), response, session)
        key = response.cookies['AIOHTTP_SESSION'].value
        request = make_mocked_request('GET', '/', headers={'Cookie': 'AIOHTTP_SESSION=' + key})
        with patch('aiohttp_session.time.time', return_value=1000059):
            current = await storage.load_session(request)
        self.assertEqual(current['user_id'], 1)
        with patch('aiohttp_session.time.time', return_value=1000061):
            expired = await storage.load_session(request)
        self.assertEqual(dict(expired), {})

    async def test_session_round_trip(self):
        storage = RedisStorage(MemoryRedis(), encoder=encode_session, decoder=decode_session)
        session = Session(None, data=None, new=True)
        payload = {'user_id': 1, 'preferences': {'theme': 'light'}}
        session.update(payload)
        response = web.Response()
        await storage.save_session(make_mocked_request('GET', '/'), response, session)
        key = response.cookies['AIOHTTP_SESSION'].value
        request = make_mocked_request('GET', '/', headers={'Cookie': 'AIOHTTP_SESSION=' + key})
        restored = await storage.load_session(request)
        self.assertEqual(dict(restored), payload)

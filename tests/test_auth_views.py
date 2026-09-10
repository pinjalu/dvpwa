from sqli.services.redis import decode_session
from tests.support import ViewCase


class AuthViewTests(ViewCase):
    async def test_logout_clears_session(self):
        await self.login()
        response = await self.client.post('/logout/', allow_redirects=False)
        self.assertEqual(response.status, 302)
        key = response.cookies['AIOHTTP_SESSION'].value
        payload = decode_session(self.app['redis'].values['AIOHTTP_SESSION_' + key])
        self.assertNotIn('user_id', payload['session'])
        # The next request must be unauthenticated using the browser's saved cookie.
        response = await self.client.post('/logout/', allow_redirects=False)
        self.assertEqual(response.status, 401)

    async def test_login_sets_session_cookie(self):
        response = await self.login()
        self.assertIn('AIOHTTP_SESSION', response.cookies)

    async def test_login_throttle_after_three(self):
        for _ in range(3):
            await self.login(password='wrong')
        response = await self.login()
        self.assertEqual(response.status, 429)

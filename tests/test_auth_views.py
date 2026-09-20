from tests.support import ViewCase


class AuthViewTests(ViewCase):
    async def test_login_sets_session_cookie(self):
        response = await self.login()
        self.assertIn('AIOHTTP_SESSION', response.cookies)

    async def test_login_throttle_after_three(self):
        for _ in range(3):
            await self.login(password='wrong')
        response = await self.login()
        self.assertEqual(response.status, 429)

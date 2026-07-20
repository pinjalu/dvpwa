from sqli.middlewares import issue_csrf_token

from aiohttp_session import get_session

from sqli.utils.auth import get_auth_user


async def csrf_processor(request):
    session = await get_session(request)

    token = None

    def csrf_token():
        nonlocal token
        if token is None:
            token = issue_csrf_token(request.app, session)
        return token

    return {'csrf_token': csrf_token}


async def auth_user_processor(request):
    auth_user = await get_auth_user(request)
    return {'auth_user': auth_user}

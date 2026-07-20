import logging
import hashlib
import hmac
import time
from uuid import uuid4

from aiohttp import web
from aiohttp.web_exceptions import HTTPForbidden, HTTPInternalServerError
from aiohttp_jinja2 import render_template
from aiohttp_session import session_middleware as session_middleware_, get_session
from aiohttp_session.redis_storage import RedisStorage

from sqli.services.redis import encode_session, decode_session
from sqli.utils.auth import session_cookie_settings

log = logging.getLogger(__name__)


@web.middleware
async def session_middleware(request, handler):
    """Wrapper to Session Middleware factory.
    """
    # Do the trick, by passing app & handler back to original session
    # middleware factory. Do not forget to await on results here as original
    # session middleware factory is also awaitable.
    app = request.app
    storage = RedisStorage(app['redis'], encoder=encode_session,
                           decoder=decode_session, **session_cookie_settings(app))
    middleware = session_middleware_(storage)
    return await middleware(request, handler)


def sign_csrf(app, value):
    secret = app['config']['app']['secret'].encode('utf-8')
    return hmac.new(secret, value.encode('ascii'), hashlib.sha256).hexdigest()


def issue_csrf_token(app, session):
    value = '{}:{}'.format(int(time.time()), uuid4().hex)
    token = value + ':' + sign_csrf(app, value)
    session['_csrf_token'] = token
    return token


@web.middleware
async def csrf_middleware(request, handler):
    if request.method == 'POST' and request.path.endswith('/review'):
        session = await get_session(request)
        expected = session.pop('_csrf_token', None)
        token = (await request.post()).get('_csrf_token', '')
        try:
            value, signature = token.rsplit(':', 1)
            issued = int(value.split(':', 1)[0])
            valid = (expected is not None
                     and hmac.compare_digest(token, expected)
                     and hmac.compare_digest(signature, sign_csrf(request.app, value))
                     and 0 <= time.time() - issued <= 3600)
        except (ValueError, TypeError, UnicodeError):
            valid = False
        if not valid:
            raise HTTPForbidden()
    return await handler(request)


def error_pages(overrides):
    @web.middleware
    async def middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override is None:
                return response
            else:
                return await override(request, response)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override is None:
                raise
            else:
                return await override(request, ex)

    return middleware


async def handle_40x(request, exc):
    response = render_template('errors/40x.jinja2',
                               request,
                               {'error': exc})
    response.set_status(exc.status)
    return response


async def handle_50x(request, exc):
    response = render_template('errors/50x.jinja2',
                               request,
                               {'error': exc})
    response.set_status(exc.status)
    return response


error_middleware = error_pages({
    x: handle_40x if x < 500 else handle_50x
    for x in range(401, 600)
})

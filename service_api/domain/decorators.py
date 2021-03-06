import asyncio
from functools import wraps
from http import HTTPStatus

from sanic.response import text, json

from service_api.domain.redis import redis


def authorized(f):
    @wraps(f)
    async def check_authorization(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Basic ') and await redis.check_session(token[6:]):
            return await f(request, *args, **kwargs)
        else:
            return text('Not authorized', HTTPStatus.UNAUTHORIZED)

    return check_authorization


def asyncio_task(f):
    @wraps(f)
    async def wraper(f, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(f(*args, **kwargs))

    return wraper

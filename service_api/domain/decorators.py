from functools import wraps

from sanic.response import text

from service_api.domain.redis import redis


def authorized(f):
    @wraps(f)
    async def check_authorization(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token and token.startswith('Basic ') and await redis.check_session(token[6:]):
            return await f(request, *args, **kwargs)
        else:
            return text('Not authorized', 401)

    return check_authorization

from http import HTTPStatus
from functools import wraps

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


def prepare_coordinates(f):
    @wraps(f)
    async def wrapper(request, *args, **kwargs):
        longitude = request.args.get('lng')
        latitude = request.args.get('lat')
        if longitude and latitude:
            longitude = longitude.replace(',', '.')
            latitude = latitude.replace(',', '.')
            return await f(request, longitude, latitude, *args, **kwargs)
        else:
            return json('Wrong coordinate parameters', HTTPStatus.UNPROCESSABLE_ENTITY)
    return wrapper

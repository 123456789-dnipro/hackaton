import binascii
import hashlib
from requests.auth import _basic_auth_str

from asyncpgsa import pg
from sanic.response import json, text

from service_api.domain.forms import LogInForm
from service_api.domain.models import users
from service_api.domain.redis import redis
from service_api.domain.utils import generate_uuid
from service_api.resources import BaseResource


class LogInResource(BaseResource):
    decorators = []

    async def post(self, request):
        data, _ = LogInForm().load(request.json)
        data['password'] = self.__hash_password(data['password'])
        users_query = await self.__get_users(data['user_name'])
        if users_query is not None:
            return await self.__login(data, users_query)

        return await self.__registration(data)

    @staticmethod
    async def __get_users(user_name):
        query = users.select().where(users.c.user_name == user_name)
        return query if await pg.fetchval(query) else None

    async def __login(self, data, query):
        async with pg.query(query) as cursor:
            async for user in cursor:
                if data['password'] == user['password']:
                    user_id = user['user_id']
                    token = self.__create_token(data['user_name'], data['password'])
                    await redis.create_session(str(user_id), token)
                    data = {
                        'user_id': str(user_id),
                        'user_name': user['user_name'],
                        'credentials': token
                    }
                    return json(data, 201)
        return text('Invalid username or/and password', 400)

    @staticmethod
    async def __registration(data):
        data['user_id'] = generate_uuid()
        query = users.insert(values=data)
        await pg.fetchrow(query)
        del data['password']
        return json(data, 201)

    @staticmethod
    def __hash_password(password):
        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)
        return binascii.hexlify(dk).decode('utf-8')

    @staticmethod
    def __create_token(user_name, password):
        return _basic_auth_str(user_name, password)[6:]

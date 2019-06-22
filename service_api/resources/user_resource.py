from asyncpgsa import pg
from sanic.response import json
from sqlalchemy.sql import select

from service_api.domain.models import users
from service_api.resources import BaseResource


class UserResource(BaseResource):

    async def get(self, request, user_id):
        q = select([users.c.user_id, users.c.user_name]).where(users.c.user_id == user_id)
        row = dict(await pg.fetchrow(q))
        row['user_id'] = str(row['user_id'])
        return json(dict(row))


class UsersResource(BaseResource):

    async def get(self, request):
        q = select([users.c.user_id, users.c.user_name])
        result = []
        async with pg.query(q) as cursor:
            async for row in cursor:
                row = dict(row)
                row['user_id'] = str(row['user_id'])
                result.append(row)
        return json(result)

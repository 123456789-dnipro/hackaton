import aioredis
from sanic import Sanic


class RedisWorker:
    def __init__(self):
        self.__host = None
        self.__pool = None

    async def init(self, app: Sanic):
        self.__host = app.config.REDIS_HOST
        self.__pool = await aioredis.create_redis(self.__host)

    async def check_session(self, token):
        print(token)
        return await self.__pool.expire(token, 300)

    async def create_session(self, user_id, token):
        await self.__pool.set(token, user_id)
        await self.__pool.expire(token, 300)
        return token

    async def close(self):
        self.__pool.close()
        await self.__pool.wait_closed()


redis = RedisWorker()

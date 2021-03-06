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
        return await self.__pool.expire(token, 300)

    async def set_conf_msg(self, phone, msg):
        await self.__pool.set(phone, msg)
        await self.__pool.expire(phone, 60)

    async def get_conf_msg(self, phone, msg):
        real_code = self.__pool.get(phone)
        if real_code == msg:
            self.__pool.delete(phone)
            return True
        else:
            return False

    async def get_user(self, token):
        return await self.__pool.get(token)

    async def create_session(self, user_id, token):
        cur_token = await self.__pool.get(user_id)
        if not cur_token:
            await self.__pool.set(token, user_id)
            await self.__pool.expire(token, 300)
        else:
            token = cur_token
        return token

    async def close(self):
        self.__pool.close()
        await self.__pool.wait_closed()


redis = RedisWorker()

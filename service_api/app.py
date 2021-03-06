from asyncpgsa import pg

from sanic import Sanic

from service_api import api
from service_api.config import AppConfig
from service_api.domain.db import get_pool
from service_api.domain.redis import redis

app = Sanic(__name__)
app.config.from_object(AppConfig)

api.load_api(app)


@app.listener('before_server_start')
async def setup_db(app, loop):
    await pg.init(app.config.DB_URI)
    await redis.init(app)


@app.listener('after_server_stop')
async def clone_connection(app, loop):
    await pg.pool.close()
    await redis.close()
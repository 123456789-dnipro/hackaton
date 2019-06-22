from sanic import Sanic

from service_api import api
from service_api.config import AppConfig
from service_api.domain.db import get_pool
from service_api.domain.redis import redis

app = Sanic(__name__)
app.config.from_object(AppConfig)

api.load_api(app)


# @app.listener('after_server_start')
# async def setup_db(app, loop):
#     app.pool = await get_pool()
#     await redis.init(app)
#
#
# @app.listener('before_server_stop')
# async def clone_connection(app, loop):
#     await app.pool.close()
#     await redis.close()
#
#
# @app.middleware('request')
# async def add_engine(request):
#     request['pool'] = app.pool

import asyncio
import os

from sanic_script import Manager

from service_api.app import app
from service_api.domain.db import init_db

manager = Manager(app)


@manager.option('-h', '--host', dest='host')
def runserver(host='0.0.0.0'):
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8000)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', '')))
#
#
# @manager.command
# def setup_db():
#     asyncio.run(init_db(app))


if __name__ == '__main__':
    manager.run()

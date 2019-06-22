import asyncio

from sanic_script import Manager

from service_api.app import app
from service_api.domain.db import init_db

manager = Manager(app)


@manager.option('-h', '--host', dest='host')
@manager.option('-p', '--port', dest='port')
def runserver(host='0.0.0.0', port=5000):
    app.run(host=host, port=port, debug=True)


@manager.command
def setup_db():
    asyncio.run(init_db(app))


if __name__ == '__main__':
    manager.run()

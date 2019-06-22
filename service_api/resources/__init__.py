from sanic.constants import HTTP_METHODS
from sanic.response import text, json
from sanic.views import HTTPMethodView

from service_api.domain.decorators import authorized


class BaseResource(HTTPMethodView):
    decorators = [authorized]

    async def options(self, request):
        methods = [m for m in HTTP_METHODS if hasattr(self, m.lower())]
        return text(None, headers={'Access-Allowed-Control-Methods': methods})


class SmokeResource(HTTPMethodView):

    async def get(self, request):
        return json({'hello': 'world'})

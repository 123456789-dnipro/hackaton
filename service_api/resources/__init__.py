import decimal
import uuid
import collections

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
        from service_api.sms_notification.send_sms import SMSNotifier
        a = SMSNotifier('registration', '380996552733', '111111', 'AE7777HH')
        await a.send_sms_message()

        return json({'hello': 'world'})

from asyncpgsa import pg
from requests.auth import _basic_auth_str
from sanic.response import json, text


from service_api.domain.forms import LogInForm
from service_api.domain.models import users
from service_api.domain.redis import redis
from service_api.domain.utils import generate_sms
from service_api.domain.utils import generate_uuid
from service_api.resources import BaseResource
from service_api.domain.sms_notifier import SMSNotifier


class LogInResource(BaseResource):
    decorators = []

    async def post(self, request):
        data, _ = LogInForm().load(request.json)
        check_request = users.select().where(users.c.phone == data['phone'])
        if await pg.fetchrow(check_request):
            if data.get('conf_code'):
                return await self.__login(data)
            else:
                return text('Confirmation code not specified', 400)

        return await self.__registration(data)

    async def __login(self, data):
        if redis.get_conf_msg(data['phone'], data['conf_code']):
            check_request = users.select().where(users.c.phone == data['phone'])
            user = await pg.fetchrow(check_request)
            token = self.__create_token(data['phone'], data['conf_code'])
            user_id = user['id']
            await redis.create_session(str(user_id), token)
            data = {
                'id': str(user_id),
                'credentials': token
            }
            return json(data, 201)
        return text('Invalid confirmation code', 400)

    @staticmethod
    async def __registration(data):
        data['id'] = generate_uuid()
        query = users.insert(values=data)
        await pg.fetchrow(query)
        code = generate_sms()
        await redis.set_conf_msg(data['phone'], code)
        sms_notifier = SMSNotifier('registration', data['phone'], str(code))
        await sms_notifier.send_sms_message()
        return json(None, 201)

    @staticmethod
    def __create_token(user_name, password):
        return _basic_auth_str(user_name, password)[6:]

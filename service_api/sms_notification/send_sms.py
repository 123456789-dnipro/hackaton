from constans import login, password, send_sms_header
from urllib.parse import urlencode
from constans import send_sms_path
import aiohttp
from jinja2 import Environment, FileSystemLoader
from sanic.log import logger

class SMSNotifier:
    def __init__(self, mode, phone, code=None, car_number=None):
        self.phone = phone
        self.mode = mode
        self.code = code
        self.car_number = car_number

    async def get_template(self):
        file_loader = FileSystemLoader('service_api/files/')
        env = Environment(loader=file_loader)
        template = env.get_template(f'{self.mode}_template.xml')

        t = template.render(username=str(login),
                            password=str(password),
                            code=self.code,
                            msg_id=str(1231231),
                            phone_number=str(self.phone),
                            car_number=str(self.car_number))
        return t

    async def translate_sms_message(self, template):
        return urlencode([('XML', template)])

    async def send_sms_message(self):
        message = await self.get_template()
        post_data = await self.translate_sms_message(message)

        async with aiohttp.ClientSession() as session:
            async with session.post(send_sms_path,
                                    data=post_data,
                                    headers=send_sms_header) as resp:
                logger.info(f"status: {resp.status} | text: {await resp.text()}")
        return self.code if self.code else self.car_number

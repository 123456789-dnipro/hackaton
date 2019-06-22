import uuid
from datetime import datetime

from asyncpgsa import pg
from sanic.log import logger

from service_api.domain.models import incedents
from service_api.domain.models import vehicles, files
from service_api.domain.sms_notifier import SMSNotifier
from service_api.domain.redis import RedisWorker


async def get_incident(incident_id):
    query = incedents.select().where(incedents.c.id == incident_id)
    incident = await pg.fetchrow(query)
    if incident:
        incident_dict = dict(incident)
        incident_dict['id'] = str(incident_dict['id'])
        incident_dict['created_by'] = str(incident_dict['created_by'])
        incident_dict['created_at'] = incident_dict['created_at'].strftime("%d/%m/%y")
    else:
        incident_dict = []
    return incident_dict

async def get_phone_number(car_number):
    query = vehicles.select().where(vehicles.c.number == car_number)
    a = await pg.fetchrow(query)
    if not a:
        return None
    else:
        return dict(a).get('number')

class Incedent:
    def __init__(self, headers):
        self.headers = headers

    async def get_incidents(self):
        return 'OK'

    async def change_incident_status(self, *args, **kwargs):
        return 'OK'

    async def report_incident(self, longitude=None, latitude=None, image=None, car_number=None,
                              comment=None):
        phone_number = await get_phone_number(car_number)
        if phone_number:
            try:
                SMSNotifier(phone=phone_number,
                            mode='notification',
                            car_number=car_number)
            except:
                logger.info('Failed to send SMS')
        incident_uuid = uuid.uuid4()
        await self.save_incedent(incident_uuid, latitude, longitude)
        await self.save_files(incident_uuid, image, comment)

        return 'YES', 200

    async def get_incident(incident_id):
        query = incedents.select().where(incedents.c.id == incident_id)
        incident = await pg.fetchrow(query)
        if incident:
            incident_dict = dict(incident)
            incident_dict['id'] = str(incident_dict['id'])
            incident_dict['created_by'] = str(incident_dict['created_by'])
            incident_dict['created_at'] = incident_dict['created_at'].strftime("%d/%m/%y")
        else:
            incident_dict = []
        return incident_dict

    async def save_incedent(self, incident_uuid, latitude, longitude, ):
        query = incedents.insert().values(id=incident_uuid,
                                          longitude_1=longitude,
                                          latitude_1=latitude,
                                          created_at=datetime.now(),
                                          created_by=await RedisWorker().get_user(self.headers().get('Authorization')))
        await pg.fetchrow(query)

    async def save_files(self, incident_uuid, image=None, comment=None, passport_data=None):
        query = files.insert().values(id=incident_uuid,
                                      name=uuid.uuid4(),
                                      data=image.body,
                                      passport_data=passport_data,
                                      user_id=await RedisWorker().get_user(self.headers().get('Authorization')))
        await pg.fetchrow(query)

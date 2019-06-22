import uuid
from datetime import datetime

from asyncpgsa import pg
from sanic.log import logger

from service_api.domain.models import incedents
from service_api.domain.models import vehicles, files
from service_api.domain.sms_notifier import SMSNotifier


async def get_phone_number(car_number):
    query = vehicles.select().where(vehicles.c.number == car_number)
    a = await pg.fetchrow(query)
    if not a:
        return None
    else:
        return dict(a).get('number')


class Incedent:
    def __init__(self):
        pass

    async def change_incident_status(self, *args, **kwargs):
        return 'OK'

    async def get_incidents(headers, longitude, latitude):
        return 'OK'

    async def report_incident(self, headers=None, longitude=None, latitude=None, image=None, car_number=None,
                              comment=None):
        phone_number = await get_phone_number(car_number)
        if phone_number:
            try:
                SMSNotifier(phone=phone_number,
                            mode='notification',
                            car_number=car_number)
            except:
                logger.info('Failed to send SMS')
        await self.save_incedent(latitude, longitude)
        await self.save_files(image, comment)

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

    async def save_incedent(self, latitude, longitude, ):
        query = incedents.insert().values(id=uuid.uuid4(),
                                          logituide=longitude,
                                          latitude=latitude,
                                          created_at=datetime.now(),
                                          created_by=await get_user_id())  # REMAKE THIS
        await pg.fetchrow(query)  # save incedent

    async def save_files(self, image=None, comment=None, passport_data=None):
        query = files.insert().values(id=uuid.uuid4(),
                                      name=uuid.uuid4(),
                                      data=image.body,
                                      passport_data=passport_data,
                                      user_id=await get_user_id()
                                      )
        await pg.fetchrow(query)  # save incedent


async def get_user_id():
    return '4fbff866-3ba5-40ca-9ed8-7ed63f0621ef'

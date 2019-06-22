import uuid
from datetime import datetime

from asyncpgsa import pg
from sqlalchemy import and_
from sanic.log import logger

from service_api.domain.models import vehicles, incedents_points
from service_api.domain.sms_notifier import SMSNotifier
from service_api.domain.redis import redis
from service_api.domain.models import incedents, files


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
    def __init__(self, auth=None):
        self.auth = auth if auth else None

    async def get_incidents(self, longitude, latitude):
        max_longitude = longitude + 0.01799
        min_longitude = longitude - 0.01799
        max_latitude = latitude + 0.01799
        min_latitude = latitude - 0.01799
        query = incedents.select().where(and_(
            incedents.c.longitude <= max_longitude, incedents.c.longitude >= min_longitude,
            incedents.c.latitude <= max_latitude, incedents.c.latitude >= min_latitude
        ))
        incidents_obj_list = await pg.fetch(query)
        incidents_list = []
        if len(incidents_obj_list) > 5:
            for incident_obj in incidents_obj_list[0: 5]:
                incident_dict = dict(incident_obj)
                query = files.select().where(files.c.id == incident_dict['id'])
                file = await pg.fetchrow(query)
                if file:
                    incident_dict['photo'] = str(dict(file)['data'])
                incident_dict['id'] = str(incident_dict['id'])
                incident_dict['created_by'] = str(incident_dict['created_by'])
                incident_dict['created_at'] = incident_dict['created_at'].strftime("%d/%m/%y")
                incidents_list.append(dict(incident_dict))
        else:
            for incident_obj in incidents_obj_list:
                incident_dict = dict(incident_obj)
                query = files.select().where(files.c.id == incident_dict['id'])
                file = await pg.fetchrow(query)
                if file:
                    incident_dict['photo'] = str(dict(file)['data'])
                incident_dict['id'] = str(incident_dict['id'])
                incident_dict['created_by'] = str(incident_dict['created_by'])
                incident_dict['created_at'] = incident_dict['created_at'].strftime("%d/%m/%y")
                incidents_list.append(dict(incident_dict))
        return incidents_list

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
        await self.save_incident(incident_uuid, latitude, longitude, comment)
        await self.save_files(incident_uuid, image, comment)

        return 'YES', 200

    async def get_incident(self, incident_id):
        query = incedents.select().where(incedents.c.id == incident_id)
        incident = await pg.fetchrow(query)
        if incident:
            incident_dict = dict(incident)
            query = files.select().where(files.c.id == incident_dict['id'])
            file = await pg.fetchrow(query)
            if file:
                incident_dict['photo'] = str(dict(file)['data'])
            incident_dict['id'] = str(incident_dict['id'])
            incident_dict['created_by'] = str(incident_dict['created_by'])
            incident_dict['created_at'] = incident_dict['created_at'].strftime("%d/%m/%y")
        else:
            incident_dict = []
        return incident_dict

    async def save_incident(self, incident_uuid, latitude, longitude, comment):
        query = incedents.insert().values(id=incident_uuid,
                                          longitude=longitude,
                                          latitude=latitude,
                                          created_at=datetime.now(),
                                          comment='12321321',
                                          created_by=self.auth)
        await pg.fetchrow(query)

    async def save_files(self, incident_uuid, image=None, comment=None, passport_data=None):
        query = files.insert().values(id=incident_uuid,
                                      name=uuid.uuid4(),
                                      data=image.body,
                                      passport_data=passport_data,
                                      user_id=self.auth)
        await pg.fetchrow(query)

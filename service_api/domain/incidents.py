from service_api.domain.models import incedents, files
from asyncpgsa import pg
from sqlalchemy import and_


async def get_incidents(longitude, latitude):
    max_longitude = longitude + 0.01799
    min_longitude = longitude - 0.01799
    max_latitude = latitude + 0.01799
    min_latitude = latitude - 0.01799
    query = incedents.select().where(and_(
        incedents.c.logituide <= max_longitude, incedents.c.logituide >= min_longitude, incedents.c.latitude <= max_latitude, incedents.c.latitude >= min_latitude
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


def report_incident(headers, longitude, latitude, image, car_number, comment):
    return 'OK', 200


async def get_incident(incident_id):
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


def change_incident_status(headers, data, incident):
    pass


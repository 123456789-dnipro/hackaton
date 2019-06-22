from service_api.domain.models import incedents
from asyncpgsa import pg


def get_incidents(headers, longitude, latitude):
    return 'OK'


def report_incident(headers, longitude, latitude, image, car_number, comment):
    return 'OK', 200


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


def change_incident_status(headers, data, incident):
    pass


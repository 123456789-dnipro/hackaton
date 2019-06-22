from http import HTTPStatus
from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.incidents import Incedent
from service_api.domain.forms import IncidentsStatusForm
from service_api.domain.decorators import prepare_coordinates


class IncidentsResource(BaseResource):
    decorators = [prepare_coordinates]

    async def get(self, request, longitude, latitude):
        incidents = Incedent.get_incidents(request.headers, longitude, latitude)
        return json(incidents, HTTPStatus.OK)

    async def post(self, request, longitude, latitude):
        image = request.files.get('image')
        car_number = request.form.get('plate_number')
        comments = request.form.get('comments')
        incident, status = await Incedent(headers=request.headers).report_incident(
                                                    longitude=float(longitude),
                                                    latitude=float(latitude), image=image,
                                                    car_number=car_number,
                                                    comment=comments)
        return json(incident, status)


class IncidentResource(BaseResource):
    decorators = []

    async def get(self, request, incident_id):
        incident = await Incedent.get_incident(incident_id)
        return json(incident, HTTPStatus.OK)

    async def put(self, request):
        data, _ = IncidentsStatusForm().load(request.json)
        incident, status = Incedent.change_incident_status(request.headers, data)
        return json(incident, status)

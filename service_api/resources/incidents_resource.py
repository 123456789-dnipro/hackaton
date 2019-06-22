from http import HTTPStatus
from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.incidents import Incedent
from service_api.domain.forms import IncidentsStatusForm
from service_api.domain.decorators import prepare_coordinates


class IncidentsResource(BaseResource):
    decorators = []

    @prepare_coordinates
    async def get(self, request, longitude, latitude):
        incidents = Incedent.get_incidents(request.headers, longitude, latitude)
        return json(incidents, HTTPStatus.OK)

    async def post(self, request):
        image = request.json.get('photo')
        car_number = request.json.get('plate')
        comments = request.json.get('comments')
        print(request.json.get('lng'))
        print(request.json.get('lat'))
        print(type(request.json.get('lat')))
        longitude = float(request.json.get('lng'))
        latitude = float(request.json.get('lat'))
        incident, status = await Incedent(headers=request.headers).report_incident(
                                                    longitude=longitude,
                                                    latitude=latitude, image=image,
                                                    car_number=car_number,
                                                    comment=comments)
        return json(incident, status)


class IncidentResource(BaseResource):
    decorators = []

    async def get(self, request, incident_id):
        incident = await Incedent().get_incident(incident_id)
        return json(incident, HTTPStatus.OK)

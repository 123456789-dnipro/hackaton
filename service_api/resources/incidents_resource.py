from http import HTTPStatus
from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.incidents import Incedent
from service_api.domain.forms import IncidentsStatusForm


class IncidentsResource(BaseResource):
    decorators = []

    async def get(self, request):
        longitude = request.args.get('lng')
        latitude = request.args.get('lat')
        if longitude and latitude:
            longitude = float(longitude.replace(',', '.'))
            latitude = float(latitude.replace(',', '.'))
        incidents = await Incedent.get_incidents(request.headers, longitude, latitude)
        return json(incidents, HTTPStatus.OK)

    async def post(self, request):
        image = request.json.get('photo')
        car_number = request.json.get('plate')
        comments = request.json.get('comments')
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

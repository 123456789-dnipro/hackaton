from http import HTTPStatus
from sanic.response import json

from service_api.resources import BaseResource
from service_api.domain.incidents import (
    get_incidents,
    report_incident,
    change_incident_status,
    get_incident
)
from service_api.domain.forms import IncidentsForm, IncidentsStatusForm
from service_api.domain.decorators import prepare_coordinates


class IncidentsResource(BaseResource):
    decorators = [prepare_coordinates]

    async def get(self, request, longitude, latitude):
        incidents = get_incidents(request.headers, longitude, latitude)
        return json(incidents, HTTPStatus.OK)

    async def post(self, request, longitude, latitude):
        data, _ = IncidentsForm().load(request.json)
        incident, status = report_incident(request.headers, data, longitude, latitude)
        return json(incident, status)


class IncidentResource(BaseResource):
    decorators = []

    async def get(self, request, incident_id):
        incident = get_incident(request.headers, incident_id)
        return json(incident, HTTPStatus.OK)

    async def put(self, request):
        data, _ = IncidentsStatusForm().load(request.json)
        incident, status = change_incident_status(request.headers, data)
        return json(incident, status)

from sanic import Blueprint
from sanic import Sanic


def load_api(app: Sanic):
    from service_api.resources import SmokeResource
    from service_api.resources.login_resource import LogInResource
    from service_api.resources.incidents_resource import IncidentResource, IncidentsResource

    api = Blueprint('v1', strict_slashes=False)

    api.add_route(SmokeResource.as_view(), '/smoke')
    api.add_route(LogInResource.as_view(), '/login')
    api.add_route(IncidentResource.as_view(), '/incidents/<incident_id:uuid>')
    api.add_route(IncidentsResource.as_view(), '/incidents')
    app.blueprint(api)

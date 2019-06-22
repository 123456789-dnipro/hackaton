from sanic import Blueprint
from sanic import Sanic


def load_api(app: Sanic):
    from service_api.resources import SmokeResource
    from service_api.resources.login_resource import LogInResource
    from service_api.resources.user_resource import UserResource, UsersResource

    api = Blueprint('v1', strict_slashes=False)

    api.add_route(SmokeResource.as_view(), '/smoke')
    api.add_route(LogInResource.as_view(), '/login')
    api.add_route(UsersResource.as_view(), '/users')
    api.add_route(UserResource.as_view(), '/users/<user_id:uuid>')

    app.blueprint(api)

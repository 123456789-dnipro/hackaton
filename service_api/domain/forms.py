from http import HTTPStatus
from marshmallow import Schema, fields
from sanic.exceptions import abort


class BaseForm(Schema):

    def handle_error(self, error, data):
        abort(HTTPStatus.UNPROCESSABLE_ENTITY, error)


class LogInForm(BaseForm):
    phone = fields.Str(required=True)
    conf_code = fields.Str()


class IncidentsStatusForm(BaseForm):
    status = fields.Str(required=True)

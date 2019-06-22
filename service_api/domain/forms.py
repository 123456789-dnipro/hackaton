from marshmallow import Schema, fields
from sanic.exceptions import abort


class BaseForm(Schema):

    def handle_error(self, error, data):
        abort(422, error)


class LogInForm(BaseForm):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
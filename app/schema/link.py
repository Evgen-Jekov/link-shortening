from app.register.extensions import marshmallow_client
from marshmallow import fields, validate, ValidationError, validates


class LinkSchema(marshmallow_client.Schema):
    id = fields.Integer(dump_only=True)
    long_link = fields.String(validate=validate.URL())
    short_link = fields.String(validate=validate.URL())
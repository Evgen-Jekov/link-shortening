from app.register.extensions import marshmallow_client
from marshmallow import fields, validate


class LinkSchema(marshmallow_client.Schema):
    id = fields.Integer(dump_only=True)
    id_user = fields.Integer(dump_only=True)
    long_link = fields.String(validate=validate.URL())
    short_link = fields.String(dump_only=True, validate=validate.URL())
from app.register.extensions import marshmallow_client
from marshmallow import fields, validate, ValidationError, validates
import re

class UserSchema(marshmallow_client.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(validate=[
        validate.Length(min=3, max=80)
    ])
    password = fields.String(load_only=True, validate=[
        validate.Length(min=6, max=100)
    ])
    email = fields.Email(validate=[validate.Length(min=0, max=50)])

    @validates('password')
    def check_password(self, password):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*;:]).+$'

        if not re.match(pattern, password):
            raise ValidationError(
                message="password should contain at one lower latter, one upper letter and one special symbol"
                )

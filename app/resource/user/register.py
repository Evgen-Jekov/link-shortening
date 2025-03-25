from flask_restful import Resource
from app.register.extensions import jwt_client

class UserRegister(Resource):
    def post(self):
        pass
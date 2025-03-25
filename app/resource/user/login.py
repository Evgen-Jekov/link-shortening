from flask_restful import Resource
from app.schema.user import UserSchema
from app.model.user import UserModel
from werkzeug.security import check_password_hash
from flask import request
from werkzeug.exceptions import Conflict, Unauthorized
from sqlalchemy.exc import SQLAlchemyError
from app.register.init_extensions import db
from app.register.init_extensions import limiter_client

class UserLogin(Resource):
    decorators = [limiter_client.limit("100/hour")]

    def post(self):
        try:
            user_data = UserSchema().load(request.get_json())
            user = UserModel.query.filter(UserModel.email==user_data['email']).first()

            if not user:
                raise Conflict('user did not found')
            
            if not check_password_hash(user.password, user_data['password']):
                raise Unauthorized('ivalid password')

            return {'message' : 'succefully login',
                     'user' : UserSchema().dump(user),
                     'token' : user.create_token()}, 200
            
        except Conflict as e:
            return {'error': str(e)}, 409
        except SQLAlchemyError as e:
            return {'error': 'Database operation failed'}, 500
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        except Unauthorized as e:
            return {'error' : str(e)}, 401
        finally:
            db.session.close()
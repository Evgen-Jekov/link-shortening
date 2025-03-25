from flask_restful import Resource
from app.schema.user import UserSchema
from app.model.user import UserModel
from flask import request
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from app.register.init_extensions import db
from werkzeug.exceptions import Conflict
from sqlalchemy.exc import SQLAlchemyError
from app.register.init_extensions import limiter_client

class UserRegister(Resource):
    decorators = [limiter_client.limit("100/hour")]

    def post(self):
        try:
            user_data = UserSchema().load(request.get_json())
            
            if UserModel.query.filter_by(email=user_data['email']).first():
                raise Conflict(description="Email already registered")
                
            user = UserModel(
                username=user_data['username'],
                email=user_data['email'],
                password=generate_password_hash(user_data['password'])
            )
            
            db.session.add(user)
            db.session.commit()
            
            return {
                'message': 'Registration successful',
                'user': UserSchema(exclude=['password']).dump(user),
                'token': user.create_token()
            }, 201
            
        except ValidationError as e:
            return {'errors': e.messages}, 400
        except Conflict as e:
            return {'error': str(e)}, 409
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'Database operation failed'}, 500
        except Exception as e:
            return {'error': 'Internal server error'}, 500
        finally:
            db.session.close()
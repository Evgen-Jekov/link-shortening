from app.model.user import UserModel
from app.schema.user import UserSchema
from app.schema.link import LinkSchema
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.register.init_extensions import limiter_client
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.register.init_extensions import db

class UserAccount(Resource):
    decorators = [limiter_client.limit("100/hour")]

    @jwt_required()
    def post(self):
        try:
            user = UserModel.query.filter(UserModel.id==get_jwt_identity()).first()
            link = user.links

            return {'user' : UserSchema().dump(user),
                    'links' : LinkSchema(many=True).dump(link)}, 200
        except SQLAlchemyError as e:
            return {'error' : str(e)}, 500
        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            db.session.close()
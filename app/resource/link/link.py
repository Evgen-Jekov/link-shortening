from flask_restful import Resource
import pyshorteners
from app.schema.link import LinkSchema
from app.register.init_extensions import redis_client
from flask_restful import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.register.init_extensions import limiter_client, ACCESS_EXPIRES, db
from app.model.link import LinkModel
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

def short_link(link):
    short = pyshorteners.Shortener()
    try:
        result = short.tinyurl.short(link)
        return result if result.startswith("http") else f"https://{result}"
    except Exception:
        return None

class Link(Resource):
    decorators = [limiter_client.limit("100/hour")]

    @jwt_required()
    def post(self):
        try:
            link_data = LinkSchema().load(request.get_json())
            
            cached = redis_client.get(link_data['long_link'])
            if cached:
                return {
                    'long_link': link_data['long_link'],
                    'short_link': cached.decode(),
                    'source': 'cache'
                }

            short = short_link(link_data['long_link'])
            if not short:
                return {'error': 'Failed to generate short URL'}, 503

            new_link = LinkModel(
                long_link=link_data['long_link'],
                short_link=short,
                id_user=int(get_jwt_identity())
            )
            
            db.session.add(new_link)
            db.session.commit()
            
            redis_client.set(link_data['long_link'], short, ex=ACCESS_EXPIRES)
            
            return {
                'detail': LinkSchema().dump(new_link),
            }, 200

        except ValidationError as e:
            return {'validation_error': str(e)}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {str(e)}")
            return {'database_error': str(e)}, 500
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return {'error': 'Internal server error'}, 500
        finally:
            db.session.close()
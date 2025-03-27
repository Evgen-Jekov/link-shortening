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
from redis.exceptions import RedisError

def short_link(link):
    short = pyshorteners.Shortener()
    try:
        result = short.tinyurl.short(link)
        return result if result.startswith("http") else f"https://{result}"
    except Exception:
        return None

class LinkCreate(Resource):
    decorators = [limiter_client.limit("100/hour")]

    @jwt_required()
    def post(self):
        try:
            link_data = LinkSchema().load(request.get_json())
            
            cached = redis_client.hget(get_jwt_identity(), link_data['long_link'])
            if cached:
                return {
                    'long_link': link_data['long_link'],
                    'short_link': cached.decode(),
                    'source': 'cache'
                }

            short = short_link(link_data['long_link'])

            if not short:
                raise Exception('Failed to generate short URL')

            new_link = LinkModel(
                long_link=link_data['long_link'],
                short_link=short,
                id_user=int(get_jwt_identity())
            )
            
            db.session.add(new_link)
            db.session.commit()
            
            redis_client.hmset(get_jwt_identity(), mapping={link_data['long_link'] : short})
            redis_client.expire(get_jwt_identity(), ACCESS_EXPIRES)
            
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
            return {'error': str(e)}, 500
        finally:
            db.session.close()


class LinkDelete(Resource):
    decorators = [limiter_client.limit("100/hour")]

    @jwt_required()
    def delete(self):
        try:
            link_data = LinkSchema().load(request.get_json())

            link = LinkModel.query.filter_by(long_link=link_data['long_link'], 
                                                          id_user=get_jwt_identity()).first()
            
            if not link:
                raise Exception('error search link')
            
            db.session.delete(link)
            db.session.commit()

            redis_client.hdel(get_jwt_identity(), link_data['long_link'])

            return {'succes delete' : 'link deleted happend successfully'}
        except ValidationError as e:
            return {'validate_error' : e.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'database_error' : str(e)}, 500
        except Exception as e:
            return {'error' : str(e)}, 400
        except RedisError as e:
            return {'redis_error' : str(e)}, 500
        finally:
            db.session.close()


class LinkPatch(Resource):
    decorators = [limiter_client.limit("100/hour")]

    @jwt_required()
    def patch(self):
        try:
            link_data = LinkSchema().load(request.get_json())
            link = LinkModel.query.filter_by(long_link=link_data['long_link'], 
                                             id_user=get_jwt_identity()).first()
            
            if not link:
                raise Exception('error search link')
            
            short = short_link(link_data['long_link'])

            if not short:
                raise Exception('Failed to generate short URL')


            link.long_link = link_data['long_link']
            link.short_link = short

            db.session.commit()

            return {'detail' : LinkSchema().dump(link)}, 200
        except ValidationError as e:
            return {'validate_error', e.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'database_error' : str(e)}, 500
        except Exception as e:
            return {'error' : str(e)}, 400
        finally:
            db.session.close()
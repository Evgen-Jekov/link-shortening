import redis
from flask_restful import Resource
from app.register.init_extensions import jwt_client
from app.register.init_extensions import jwt_redis
from flask_jwt_extended import get_jwt, jwt_required
from app.register.init_extensions import ACCESS_EXPIRES

@jwt_client.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis.get(jti)
    return token_in_redis is not None

class UserLogout(Resource):


    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        jwt_redis.set(jti, 'revoked', ex=ACCESS_EXPIRES)
        return {"msg" : "Access token revoked"}, 200

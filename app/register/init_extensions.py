from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

jwt_client = JWTManager()
db = SQLAlchemy()
migrate_client = Migrate()
redis_client = FlaskRedis()
marshmallow_client = Marshmallow()
limiter_client = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"])

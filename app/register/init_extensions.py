from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

jwt_client = JWTManager()
db_client = SQLAlchemy()
migrate_client = Migrate()
redis_client = FlaskRedis()

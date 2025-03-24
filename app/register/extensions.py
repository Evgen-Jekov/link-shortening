from app.register.config import Config
from app.register.init_extensions import db_client, migrate_client, jwt_client, redis_client

def extensions_connect(app):
    app.config.from_object(Config)

    db_client.init_app(app=app)
    jwt_client.init_app(app=app)
    redis_client.init_app(app)

    migrate_client.init_app(app=app, db=db_client)



    
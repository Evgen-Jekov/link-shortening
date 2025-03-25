from app.register.init_extensions import db_client, migrate_client, jwt_client, redis_client, marshmallow_client
from app.model.link import LinkModel
from app.model.user import UserModel

def extensions_connect(app):
    db_client.init_app(app=app)
    jwt_client.init_app(app=app)
    redis_client.init_app(app=app)
    marshmallow_client.init_app(app=app)

    migrate_client.init_app(app=app, db=db_client)



    
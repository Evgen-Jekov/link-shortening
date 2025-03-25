from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.register.extensions import extensions_connect
from config import Config

def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    app.config.from_object(Config)

    extensions_connect(app=app)

    return app

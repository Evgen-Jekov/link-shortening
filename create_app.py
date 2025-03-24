from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.register.extensions import extensions_connect

def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app)

    extensions_connect(app=app)

    return app

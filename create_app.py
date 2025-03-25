from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.register.extensions import extensions_connect
from config import Config
from app.resource.register_route import connect_roat_to_api

def create_app():
    app = Flask(__name__)
    api = Api(app)
    CORS(app, 
         resources={r"/link/*": {"origins": ["http://127.0.0.1:5000", "http://localhost:5000"]}})

    app.config.from_object(Config)

    extensions_connect(app=app)
    connect_roat_to_api(api=api)

    return app

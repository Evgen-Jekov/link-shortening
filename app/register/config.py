import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL')
    DEBUG = True
    REDIS_URL = os.getenv('REDIS')
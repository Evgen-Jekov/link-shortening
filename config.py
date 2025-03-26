import os

class Config:
    """
    Class is for application configuration.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('SQL')
    DEBUG = True
    REDIS_URL = os.getenv('REDIS')
    JWT_SECRET_KEY = os.getenv('JWT')

TTL = 24 * 60 * 60
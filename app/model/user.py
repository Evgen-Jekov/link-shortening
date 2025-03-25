from app.register.extensions import db_client
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token

class UserModel(db_client.Model):
    __tablename__ = 'user'

    id = db_client.Column(db_client.Integer, primary_key=True)
    username = db_client.Column(db_client.String(80), nullable=False)
    email = db_client.Column(db_client.String(50), unique=True, nullable=False)
    password = db_client.Column(db_client.String(255), nullable=False)

    link = db_client.relationship('LinkModel', backref='user', lazy='dynamic')



    def create_token(self, expire_time=3600):
        time = timedelta(seconds=expire_time)
        ref_time = timedelta(seconds=expire_time*5)
        token = create_access_token(
                identity=str(self.id),
                additional_claims={
                "username" : self.username,
                "email" : self.email
                },
                expires_delta=time)
    
        refresh_token = create_refresh_token(identity=self.id, expires_delta=ref_time)

        return {"token" : token, "refresh_token" : refresh_token}
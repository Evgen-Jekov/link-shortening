from app.register.extensions import db
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    links = db.relationship('LinkModel', back_populates='user', lazy='dynamic')



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
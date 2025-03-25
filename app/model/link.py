from app.register.init_extensions import db

class LinkModel(db.Model):
    __tablename__ = 'link'

    id = db.Column(db.Integer, primary_key=True)
    long_link = db.Column(db.String, nullable=False)
    short_link = db.Column(db.String, nullable=False)

    user = db.relationship('UserModel', back_populates='links')
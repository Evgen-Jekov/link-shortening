from app.register.init_extensions import db_client

class LinkModel(db_client.Model):
    __tablename__ = 'link'

    id = db_client.Column(db_client.Integer, primary_key=True)
    long_link = db_client.Column(db_client.String, nullable=False)
    short_link = db_client.Column(db_client.String, nullable=False)

    user_id = db_client.Column(db_client.Integer, db_client.ForeignKey('user.id'))
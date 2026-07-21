from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True)

    password = db.Column(db.String(255))

    role = db.Column(db.String(20), default="scanner")

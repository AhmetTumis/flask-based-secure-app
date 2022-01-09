from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(12))
    feedback = db.Column(db.String(1000))
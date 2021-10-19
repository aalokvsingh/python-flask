from database import db
import datetime

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.datetime.utcnow)

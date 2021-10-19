from database import db
import datetime

class MasterProduct(db.Model):
    __tablename__ = "master_product"
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255))
    status = db.Column(db.Integer)
    parent_product_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime,onupdate=datetime.datetime.utcnow)

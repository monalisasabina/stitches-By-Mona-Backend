from models import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'

    id               = db.Column(db.Integer, primary_key=True)
    firstname        = db.Column(db.String(50), nullable=False)
    lastname         = db.Column(db.String(50), nullable=False)
    email            = db.Column(db.String(120), unique=True, nullable=False)
    phone            = db.Column(db.String(20), nullable=True)
    delivery_address = db.Column(db.Text, nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    orders        = db.relationship('Order', back_populates='customer', lazy=True)
    custom_orders = db.relationship('CustomOrder', back_populates='customer', lazy=True)

    def to_dict(self):
        return {
            'id':               self.id,
            'firstname':        self.firstname,
            'lastname':         self.lastname,
            'email':            self.email,
            'phone':            self.phone,
            'delivery_address': self.delivery_address,
            'created_at':       self.created_at.isoformat(),
        }
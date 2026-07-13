from models import db
from datetime import datetime
import bcrypt

class Customer(db.Model):
    __tablename__ = 'customers'

    id               = db.Column(db.Integer, primary_key=True)
    firstname        = db.Column(db.String(50), nullable=False)
    lastname         = db.Column(db.String(50), nullable=False)
    username         = db.Column(db.String(50), unique=True, nullable=True)  
    email            = db.Column(db.String(120), unique=True, nullable=True)
    phone            = db.Column(db.String(20), nullable=True)
    delivery_address = db.Column(db.Text, nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash      = db.Column(db.String(128), nullable=True)  

    # to check if customer is deleted
    is_deleted       = db.Column(db.Boolean, default=False)

    # relationships
    orders        = db.relationship('Order', back_populates='customer', lazy=True)
    custom_orders = db.relationship('CustomOrder', back_populates='customer', lazy=True)


    #Setting password for customers 
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    # Checking password
    def check_password(self, password):
        if not self.password_hash:
            return False
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    
    def to_dict(self):
        return {
            'id':               self.id,
            'firstname':        self.firstname,
            'lastname':         self.lastname,
            'username':         self.username,
            'email':            self.email,
            'phone':            self.phone,
            'delivery_address': self.delivery_address,
            'created_at':       self.created_at.isoformat(),
        }
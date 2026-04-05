from models import db
from datetime import datetime

class CustomOrder(db.Model):
    __tablename__ = 'custom_orders'

    id               = db.Column(db.Integer, primary_key=True)
    customer_id      = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_description = db.Column(db.Text, nullable=False)
    yarn_preference  = db.Column(db.String(100), nullable=True)
    color_preference = db.Column(db.String(100), nullable=True)
    size_notes       = db.Column(db.Text, nullable=True)
    budget           = db.Column(db.Float, nullable=True)
    deadline         = db.Column(db.DateTime, nullable=True)
    status           = db.Column(db.String(30), default='received')
    admin_notes      = db.Column(db.Text, nullable=True)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='custom_orders')

    def to_dict(self):
        return {
            'id':               self.id,
            'customer_id':      self.customer_id,
            'item_description': self.item_description,
            'yarn_preference':  self.yarn_preference,
            'color_preference': self.color_preference,
            'size_notes':       self.size_notes,
            'budget':           self.budget,
            'deadline':         self.deadline.isoformat() if self.deadline else None,
            'status':           self.status,
            'admin_notes':      self.admin_notes,
            'created_at':       self.created_at.isoformat(),
        }
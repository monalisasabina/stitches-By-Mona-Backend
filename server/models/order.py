from models import db
from datetime import datetime

# Order is the receipt. It represents the entire purchase
class Order(db.Model):
    __tablename__ = 'orders'

    id          = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status      = db.Column(db.String(30), default='pending')
    # pending → confirmed → shipped → delivered → cancelled
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='orders')
    items    = db.relationship('OrderItem', back_populates='order', lazy=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'customer_id':  self.customer_id,
            'total_amount': self.total_amount,
            'status':       self.status,
            'created_at':   self.created_at.isoformat(),
            'items':        [item.to_dict() for item in self.items],
        }


# OrderItem represents each individual product in the order, along with quantity.
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)

    order   = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')

    def to_dict(self):
        return {
            'id':         self.id,
            'order_id':   self.order_id,
            'product_id': self.product_id,
            'quantity':   self.quantity,
            'unit_price': self.unit_price,
            'subtotal':   self.quantity * self.unit_price,
        }
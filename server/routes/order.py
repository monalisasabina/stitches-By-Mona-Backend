from flask import request
from flask_restful import Resource
from models import db
from models.order import Order, OrderItem
from models.product import Product
from models.customer import Customer

class OrderList(Resource):
    def get(self):
        orders = Order.query.all()
        return [o.to_dict() for o in orders], 200
    

    def post(self):
        data = request.get_json()

        # validate customer
        customer_id = data.get('customer_id')
        if not customer_id:
            return {'error': 'customer_id is required'}, 400

        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404

        # validate items
        items = data.get('items', [])
        if not items:
            return {'error': 'Order must have at least one item'}, 400

        # create the order
        order = Order(
            customer_id  = customer_id,
            total_amount = 0,  # will calculate below
            status       = 'pending',
        )
        db.session.add(order)
        db.session.flush()  # get order.id before committing

        # create order items and calculate total
        total = 0
        for item in items:
            product = Product.query.get(item.get('product_id'))
            if not product:
                return {'error': f'Product {item.get("product_id")} not found'}, 404
            if not product.is_available:
                return {'error': f'{product.name} is not available'}, 400
            if product.stock < item.get('quantity', 1):
                return {'error': f'Not enough stock for {product.name}'}, 400

            order_item = OrderItem(
                order_id   = order.id,
                product_id = product.id,
                quantity   = item.get('quantity', 1),
                unit_price = product.price,  # lock in price at time of order
            )
            db.session.add(order_item)

            # deduct stock
            product.stock -= item.get('quantity', 1)

            # add to total
            total += product.price * item.get('quantity', 1)

        # update total
        order.total_amount = total
        db.session.commit()
        return order.to_dict(), 201


from flask import request
from flask_restful import Resource
from server.scripts import db
from models.custom_order import CustomOrder
from models.customer import Customer
from datetime import datetime

class CustomOrderList(Resource):

    # Getting all custome orders
    def get(self):
        custom_orders = CustomOrder.query.all()
        return [co.to_dict() for co in custom_orders], 200
    
    # Creating a new custom order
    def post(self):
        data = request.get_json()

        # validate customer
        customer_id = data.get('customer_id')
        if not customer_id:
            return {'error': 'customer_id is required'}, 400

        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404

        # validate description
        if not data.get('item_description'):
            return {'error': 'item_description is required'}, 400

        # parse deadline if provided
        deadline = None
        if data.get('deadline'):
            try:
                deadline = datetime.strptime(data.get('deadline'), '%Y-%m-%d')
                # strptime: converts a string representing a date and time into datetime object
                # '%Y-%m-%d': format string that represents a date in the format of year-month-day (e.g., 2024-12-31)
            except ValueError:
                return {'error': 'deadline must be in YYYY-MM-DD format'}, 400
     

        custom_order = CustomOrder(
            customer_id      = customer_id,
            item_description = data.get('item_description'),
            yarn_preference  = data.get('yarn_preference'),
            color_preference = data.get('color_preference'),
            size_notes       = data.get('size_notes'),
            budget           = data.get('budget'),
            deadline         = deadline,
            status           = 'received',
        )

        db.session.add(custom_order)
        db.session.commit()
        return custom_order.to_dict(), 201
    

class CustomOrderDetail(Resource):

    # Getting a single custom order by ID
    def get(self, id):

        custom_order = CustomOrder.query.get(id)
        if not custom_order:
            return {'error': 'Custom order not found'}, 404
        return custom_order.to_dict(), 200
    

    def patch(self, id):

        custom_order = CustomOrder.query.get(id)
        if not custom_order:
            return {'error': 'Custom order not found'}, 404

        data = request.get_json()

        allowed_statuses = ['received', 'reviewing', 'quoted', 'in_progress', 'ready', 'delivered']

        if 'customer_id' in data:
            customer = Customer.query.get(data['customer_id'])
            if not customer:
                return {'error': 'Customer not found'}, 404
            custom_order.customer_id = data['customer_id']

        if 'item_description' in data: custom_order.item_description = data['item_description']
        if 'yarn_preference'  in data: custom_order.yarn_preference  = data['yarn_preference']
        if 'color_preference' in data: custom_order.color_preference = data['color_preference']
        if 'size_notes'       in data: custom_order.size_notes       = data['size_notes']
        if 'budget'           in data: custom_order.budget           = data['budget']
        if 'admin_notes'      in data: custom_order.admin_notes      = data['admin_notes']
        if 'status' in data:
            if data['status'] not in allowed_statuses:
                return {'error': f'Status must be one of {allowed_statuses}'}, 400
            custom_order.status = data['status']
        if 'deadline' in data:
            try:
                custom_order.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d')
            except ValueError:
                return {'error': 'deadline must be in YYYY-MM-DD format'}, 400

        db.session.commit()
        return custom_order.to_dict(), 200
    
    # Deleting a custom order
    def delete(self, id):
        custom_order = CustomOrder.query.get(id)
        if not custom_order:
            return {'error': 'Custom order not found'}, 404

        db.session.delete(custom_order)
        db.session.commit()
        return {'message': 'Custom order deleted successfully'}, 200
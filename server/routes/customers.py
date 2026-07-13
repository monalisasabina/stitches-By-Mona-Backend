from flask import request
from flask_restful import Resource
from models import db
from models.customer import Customer


class Customers(Resource):
     
    #  Getting customer list
    def get(self):
        customers = Customer.query.all()
        return [c.to_dict() for c in customers], 200
     

    # Adding a new customer
    def post(self):
        data = request.get_json()

        if not data.get('firstname') or not data.get('lastname') or not data.get('email'):
            return {'error': 'firstname, lastname and email are required'}, 400

        # check if email already exists
        existing = Customer.query.filter_by(email=data.get('email')).first()
        if existing:
            return {'error': 'A customer with that email already exists'}, 409

        customer = Customer(
            firstname        = data.get('firstname'),
            lastname         = data.get('lastname'),
            username         = data.get('username'),
            password_hash    = data.get('password'),  
            email            = data.get('email'),
            phone            = data.get('phone'),
            delivery_address = data.get('delivery_address'),
        )
        db.session.add(customer)
        db.session.commit()
        return customer.to_dict(), 201


class CustomerDetail(Resource):

    # Getting a single customer by ID
    def get(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        return customer.to_dict(), 200
    
    # Updating a customer
    def patch(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
    
        data = request.get_json()

        if 'firstname'        in data: customer.firstname        = data['firstname']
        if 'lastname'         in data: customer.lastname         = data['lastname']
        if 'username'         in data: customer.username         = data['username']
        if 'email'            in data: customer.email            = data['email']
        if 'phone'            in data: customer.phone            = data['phone']
        if 'delivery_address' in data: customer.delivery_address = data['delivery_address']

        db.session.commit()
        return customer.to_dict(), 200
    
    # Deleting a customer
    def delete(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        # soft delete a customer
        customer.is_deleted = True

        # remove personal information for privacy
        customer.email = None
        customer.phone = None
        customer.username = None
        customer.delivery_address = None
        customer.password_hash = None

        db.session.commit()
        return {'message': f'{customer.firstname} {customer.lastname} deleted successfully'}, 200

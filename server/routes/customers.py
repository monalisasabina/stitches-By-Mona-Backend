from flask import request
from flask_restful import Resource
from models import db
from models.customer import Customer


class Customers(Resource):
     
    #  Getting customer list
    def get(self):
        customers = Customer.query.filter_by(is_deleted=False).all()
        return [c.to_dict() for c in customers], 200
     

    # Adding a new customer
    def post(self):
        data = request.get_json()

        if not data.get('firstname') or not data.get('lastname') or not data.get('email'):
            return {'error': 'firstname, lastname and email are required'}, 400

        # check if email already exists
        existing_email = Customer.query.filter_by(email=data.get('email')).first()
        if existing_email:
            return {'error': 'A customer with that email already exists'}, 409

        # check if username already exists
        existing_username = Customer.query.filter_by(username=data.get('username')).first()
        if existing_username:
            return {'error': 'A customer with that username already exists'}, 409

        customer = Customer(
            firstname        = data.get('firstname'),
            lastname         = data.get('lastname'),
            username         = data.get('username'),  
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
        customer = Customer.query.filter_by(id=id, is_deleted=False).first()
        if not customer:
            return {'error': 'Customer not found'}, 404
        return customer.to_dict(), 200
    
    # Updating a customer
    def patch(self, id):
        customer = Customer.query.filter_by(id=id, is_deleted=False).first()
        if not customer:
            return {'error': 'Customer not found'}, 404
        
    
        data = request.get_json()

        if 'firstname'        in data: customer.firstname        = data['firstname']
        if 'lastname'         in data: customer.lastname         = data['lastname']
        if 'phone'            in data: customer.phone            = data['phone']
        if 'delivery_address' in data: customer.delivery_address = data['delivery_address']

        # username
        if 'username'         in data: 

            # checking if username exists for another customer
            existing_username = Customer.query.filter_by(username=data['username']).first()
            if existing_username and existing_username.id != id:
                return {'error': 'A customer with that username already exists'}, 409
            
            customer.username         = data['username']

        # email
        if 'email'            in data: 

            # checking if email exists for another customer
            existing_email = Customer.query.filter_by(email=data['email']).first()
            if existing_email and existing_email.id != id:
                return {'error': 'A customer with that email already exists'}, 409

            customer.email            = data['email']

        db.session.commit()

        return customer.to_dict(), 200
    
    # Deleting a customer
    def delete(self, id):

        customer = Customer.query.filter_by(id=id, is_deleted=False).first()

        if not customer:
            return {'error': 'Customer not found'}, 404

        customer.is_deleted = True
        
        db.session.commit()
        return {'message': f'{customer.firstname} {customer.lastname} deleted successfully'}, 200

# Show deleted customers
class DeletedCustomers(Resource):
    def get(self):

        deleted_customers = Customer.query.filter_by(is_deleted=True).all()

        return [c.to_dict() for c in deleted_customers], 200

# Restored Customer
class RestoreCustomer(Resource):
    def patch(self, id):
        customer = Customer.query.filter_by(id=id, is_deleted=True).first()

        if not customer:
            return {'error': 'Customer not found or not deleted'}, 404

        customer.is_deleted = False

        db.session.commit()

        return {
            'message': f'{customer.firstname} {customer.lastname} restored successfully',
            'customer': customer.to_dict()
        }, 200

      

     
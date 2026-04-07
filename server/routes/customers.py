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
            email            = data.get('email'),
            phone            = data.get('phone'),
            delivery_address = data.get('delivery_address'),
        )
        db.session.add(customer)
        db.session.commit()
        return customer.to_dict(), 201


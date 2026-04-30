from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.customer import Customer

class CustomerRegister(Resource):
    def post(self):
        data = request.get_json()

        # validate required fields
        if not data.get('firstname') or not data.get('lastname'):
            return {'error': 'firstname and lastname are required'}, 400
        if not data.get('email'):
            return {'error': 'email is required'}, 400
        if not data.get('password'):
            return {'error': 'password is required'}, 400

        # check if email already exists
        if Customer.query.filter_by(email=data.get('email')).first():
            return {'error': 'email already registered'}, 409

        # check if username already exists
        if Customer.query.filter_by(username=data.get('username')).first():
            return {'error': 'username already taken'}, 409

        # create customer
        customer = Customer(
            firstname        = data.get('firstname'),
            lastname         = data.get('lastname'),
            username         = data.get('username'),
            email            = data.get('email'),
            phone            = data.get('phone'),
            delivery_address = data.get('delivery_address'),
        )
        customer.set_password(data.get('password'))

        db.session.add(customer)
        db.session.commit()

        # generate token immediately after register
        token = create_access_token(identity={
            'id':   customer.id,
            'role': 'customer'
        })

        return {
            'message':  'Account created successfully',
            'token':    token,
            'customer': customer.to_dict()
        }, 201


class CustomerLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'error': 'email and password are required'}, 400

        customer = Customer.query.filter_by(email=data.get('email')).first()

        # check customer exists and password is correct
        if not customer or not customer.check_password(data.get('password')):
            return {'error': 'invalid email or password'}, 401

        token = create_access_token(identity={
            'id':   customer.id,
            'role': 'customer'
        })

        return {
            'message':  'Login successful',
            'token':    token,
            'customer': customer.to_dict()
        }, 200


class CustomerProfile(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()

        if identity['role'] != 'customer':
            return {'error': 'Unauthorized'}, 403

        customer = Customer.query.get(identity['id'])
        if not customer:
            return {'error': 'Customer not found'}, 404

        return customer.to_dict(), 200
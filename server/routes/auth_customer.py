from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.customer import Customer


class CustomerLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'error': 'email and password are required'}, 400

        customer = Customer.query.filter_by(email=data.get('email')).first()

        if not customer or not customer.check_password(data.get('password')):
            return {'error': 'invalid email or password'}, 401

        # shorter expiry for customer — 8 hours
        token = create_access_token(
            identity={'id': customer.id, 'role': 'customer'},
            expires_delta=timedelta(hours=8)
        )

        return {
            'message': 'Customer login successful',
            'token':   token,
            'customer':   customer.to_dict()
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
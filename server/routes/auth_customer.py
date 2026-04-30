from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.admin import Admin

class AdminLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'error': 'email and password are required'}, 400

        admin = Admin.query.filter_by(email=data.get('email')).first()

        if not admin or not admin.check_password(data.get('password')):
            return {'error': 'invalid email or password'}, 401

        # shorter expiry for admin — 8 hours
        token = create_access_token(
            identity={'id': admin.id, 'role': 'admin'},
            expires_delta=timedelta(hours=8)
        )

        return {
            'message': 'Admin login successful',
            'token':   token,
            'admin':   admin.to_dict()
        }, 200


class AdminProfile(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()

        if identity['role'] != 'admin':
            return {'error': 'Unauthorized'}, 403

        admin = Admin.query.get(identity['id'])
        if not admin:
            return {'error': 'Admin not found'}, 404

        return admin.to_dict(), 200
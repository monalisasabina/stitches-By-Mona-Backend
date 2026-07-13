from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from server.models import db
from models.admin import Admin

class AdminRegister(Resource):
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()

        # only super admin can create other admins
        if identity['role'] != 'admin':
            return {'error': 'Unauthorized'}, 403

        # check if the logged in admin is super admin
        logged_in_admin = Admin.query.get(identity['id'])

        if not logged_in_admin.is_super_admin:
            return {'error': 'Only the super admin can create new admins'}, 403

        data = request.get_json()

        if not data.get('firstname') or not data.get('lastname'):
            return {'error': 'firstname and lastname are required'}, 400
        if not data.get('email'):
            return {'error': 'email is required'}, 400
        if not data.get('password'):
            return {'error': 'password is required'}, 400
        if not data.get('username'):
            return {'error': 'username is required'}, 400
        
        # To avoid duplicate  username
        if Admin.query.filter_by(username=data.get('username')).first():
            return {'error': 'username already registered'}, 409

        # check if email already exists
        if Admin.query.filter_by(email=data.get('email')).first():
            return {'error': 'email already registered'}, 409

        new_admin = Admin(
            firstname      = data.get('firstname'),
            lastname       = data.get('lastname'),
            username       = data.get('username'),
            email          = data.get('email'),
            is_super_admin = False,  # staff are never super admin
        )
        new_admin.set_password(data.get('password'))

        db.session.add(new_admin)
        db.session.commit()

        return {
            'message': 'Admin created successfully',
            'admin':   new_admin.to_dict()
        }, 201


class AdminLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'error': 'email and password are required'}, 400

        admin = Admin.query.filter_by(email=data.get('email')).first()

        if not admin or not admin.check_password(data.get('password')):
            return {'error': 'invalid email or password'}, 401

        token = create_access_token(
            identity={
                'id':             admin.id,
                'role':           'admin',
                'is_super_admin': admin.is_super_admin
            },
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
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from models import db
from models.admin import Admin

BLOCKLIST = set()  # This should be imported from your main application context where it's defined

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

        identifier = data.get('identifier')  # email or username
        password = data.get('password')

        if not identifier or not password:
            return {'error': 'identifier and password are required'}, 400

        admin = Admin.query.filter(
            (Admin.email == identifier) | (Admin.username == identifier)
        ).first()

        if not admin or not admin.check_password(data.get('password')):
            return {'error': 'invalid email or password'}, 401

        token = create_access_token(
            identity=str(admin.id),   # just the ID
            additional_claims={
            "role": "admin",
            "is_super_admin": admin.is_super_admin
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

class AdminUpdate(Resource):
    @jwt_required()

    # Updating an admin
    def patch(self, id):

        identity = get_jwt_identity() # Get the logged-in admin's ID from the JWT
        if not identity:
            return {'error': 'Unauthorized'}, 403

        admin = Admin.query.filter_by(id=id).first()
    
        if not admin:
            return {'error': 'Admin not found'}, 404
    
    
        data = request.get_json()
    
        if 'firstname'        in data: admin.firstname        = data['firstname']
        if 'lastname'         in data: admin.lastname         = data['lastname']
    
        # username
        if 'username'         in data: 
    
            # checking if username exists for another admin
            existing_username = Admin.query.filter_by(username=data['username']).first()
            if existing_username and existing_username.id != id:
                return {'error': 'An admin with that username already exists'}, 409
    
            admin.username         = data['username']
    
        # email
        if 'email'            in data: 
    
            # checking if email exists for another customer
            existing_email = Admin.query.filter_by(email=data['email']).first()
            if existing_email and existing_email.id != id:
                return {'error': 'An admin with that email already exists'}, 409
    
            admin.email            = data['email']
    
        db.session.commit()
    
        return admin.to_dict(), 200
    

class AdminChangePassword(Resource):
    @jwt_required()
    def patch(self):

        # Get the logged-in admin's identity from the JWT
        claims = get_jwt()

        if claims['role'] != 'admin':
           return {'error': 'Unauthorized'}, 403

        admin_id = get_jwt_identity()  # Get the logged-in admin's ID from the JWT

        admin = Admin.query.filter_by(id=admin_id).first()

        if not admin:
            return {'error': 'Admin not found'}, 404

        data = request.get_json()

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # checks if the old password is there
        if not old_password:
            return {'error': 'old_password is required'}, 400

        # checks if the new password is there
        if not new_password:
            return {'error': 'new_password is required'}, 400

        # checks if the old password is correct
        if not admin.check_password(old_password):
            return {'error': 'Old password is incorrect'}, 401

        # checks if the new password is different from the old password
        if admin.check_password(new_password):
            return {'error': 'New password cannot be the same as the old password'}, 400
        
        # checks if the new password is at least 8 characters long
        if len(new_password) < 8:
            return {'error': 'New password must be at least 8 characters long'}, 400

        admin.set_password(new_password)
        db.session.commit()

        return {'message': 'Password changed successfully'}, 200



class AdminLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']  # Get the unique identifier for the JWT
        BLOCKLIST.add(jti)  # Add the jti to the blocklist to revoke the token
        return {'message': 'Admin logged out successfully'}, 200
# Route for displaying the admins list

from flask import request
from flask_restful import Resource
from models import db
from models.admin import Admin

class Admins(Resource):
    def get(self):
        
        admins = Admin.query.all()
        return [admin.to_dict() for admin in admins], 200


class AdminDetail(Resource):
    def get(self, id):
        admin = Admin.query.get(id)
        if not admin:
            return {'error': 'Admin not found'}, 404
        return admin.to_dict(), 200
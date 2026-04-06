from flask import request
from flask_restful import Resource
from models import db
from models.product import Product

class Products(Resource):

    def get(self):
        products = Product.query.all()
        return [product.to_dict() for product in products], 200
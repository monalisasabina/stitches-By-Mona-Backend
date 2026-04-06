from flask import request
from flask_restful import Resource
from models import db
from models.product import Product

class Products(Resource):

    # Getting the products
    def get(self):
        products = Product.query.all()
        return [product.to_dict() for product in products], 200
    
    # Adding a new product
    def post(self):
        data = request.get_json()

        if not data.get('name') or not data.get('price') or not data.get('category'):
            return {'error': 'name, price and category are required'}, 400

        product = Product(
            name         = data.get('name'),
            description  = data.get('description'),
            price        = data.get('price'),
            stock        = data.get('stock', 0),
            image_url    = data.get('image_url'),
            category     = data.get('category'),
            is_available = data.get('is_available', True),
        )
        db.session.add(product)
        db.session.commit()
        return product.to_dict(), 201
    
class Products_By_ID(Resource):

    # Getting a product by ID
    def get(self, id):
        product = Product.query.get(id)
        if not product:
            return {'error': 'Product not found'}, 404
        return product.to_dict(), 200
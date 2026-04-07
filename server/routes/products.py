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
    
    # Updating a product by ID
    def patch(self, id):
        product = Product.query.get(id)

        if not product:
            return {'error': 'Product not found'}, 404

        data = request.get_json()

        if 'name'         in data: product.name         = data['name']
        if 'description'  in data: product.description  = data['description']
        if 'price'        in data: product.price        = data['price']
        if 'stock'        in data: product.stock        = data['stock']
        if 'image_url'    in data: product.image_url    = data['image_url']
        if 'category'     in data: product.category     = data['category']
        if 'is_available' in data: product.is_available = data['is_available']

        db.session.commit()
        return product.to_dict(), 200
    
    # Deleting a product by ID
    def delete(self, id):
        product = Product.query.get(id)
        if not product:
            return {'error': 'Product not found'}, 404

        db.session.delete(product)
        db.session.commit()
        return {'message': f'{product.name} deleted successfully'}, 200
    

class ProductByCategory(Resource):
    def get(self, category):
        products = Product.query.filter_by(category=category).all()
        return [p.to_dict() for p in products], 200
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from models import db
from config import Config

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    return app

app = create_app()

api = Api(app)
CORS(app)

# -----------------------------------------------------------
# ENDPOINTS

# Home endpoint 
from routes.home import Home
api.add_resource(Home, '/')


# Product endpoints
from routes.products import Products, Products_By_ID, ProductByCategory

api.add_resource(Products, '/products')
api.add_resource(Products_By_ID, '/products/<int:id>')  
api.add_resource(ProductByCategory, '/products/category/<string:category>')


# Customer endpoints
from routes.customers import Customers, CustomerDetail

api.add_resource(Customers, '/customers')   
api.add_resource(CustomerDetail, '/customers/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
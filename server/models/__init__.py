from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()

from models.product import Product
from models.order import Order
from models.custom_order import CustomOrder
from models.customer import Customer


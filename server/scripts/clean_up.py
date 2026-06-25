from run import app
from server.scripts import db
from models.customer import Customer
from models.product import Product
from models.order import Order, OrderItem
from models.custom_order import CustomOrder
from models.admin import Admin


with app.app_context():

    # Delete all records from the Admin table except for the super admin
    db.session.query(Admin).filter(Admin.is_super_admin == False).delete()


    # Delete all records from the tables
    db.session.query(OrderItem).delete()
    db.session.query(Order).delete()
    db.session.query(CustomOrder).delete()
    db.session.query(Product).delete()
    db.session.query(Customer).delete()

    # Commit the changes to the database
    db.session.commit()

    print("All records deleted successfully.")
# super_admin.py: ensures that a super admin is created when the application starts, if one does not already exist. It reads the super admin's details from environment variables and uses the Admin model to create and store the super admin in the database.

# --------------------------------------------------------------------------------------------------------------

import os
from dotenv import load_dotenv
from run import app
from models import db
from models.admin import Admin

load_dotenv(override=True)  # Load environment variables from .env file

def create_super_admin():
     
     # with app.app_context(): is used to ensure that the code runs within the application context, which is necessary for database operations in Flask. 
     with app.app_context():
          
        # check if super admin already exists
        existing = Admin.query.filter_by(email=os.getenv('ADMIN_EMAIL')).first()

        if existing:
            print('Super admin already exists')
            return  
        
        admin = Admin(
            firstname      = os.getenv('ADMIN_FIRSTNAME'),
            lastname       = os.getenv('ADMIN_LASTNAME'),
            username       = os.getenv('ADMIN_USERNAME'),
            email          = os.getenv('ADMIN_EMAIL'),
            phone          = os.getenv('ADMIN_PHONE'),
            is_active      = True,
            is_super_admin = True,  
        )
        # admin.set_password(os.getenv('ADMIN_PASSWORD'))

        password = os.getenv('ADMIN_PASSWORD')
        # print("Password from environment variable:", password)

        # print("Password exists:", password is not None)
        # print("Password length:", len(password) if password else 0)

        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print('Super admin created successfully')

if __name__ == '__main__':
    create_super_admin()
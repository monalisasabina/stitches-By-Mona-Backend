import os
from dotenv import load_dotenv
from run import app
from server.scripts import db
from models.admin import Admin

load_dotenv()   

def create_super_admin():
     
     #   
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
            is_super_admin = True,  
        )
        admin.set_password(os.getenv('ADMIN_PASSWORD'))
        db.session.add(admin)
        db.session.commit()

        print('Super admin created successfully')

if __name__ == '__main__':
    create_super_admin()
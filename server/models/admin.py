from models import db
from datetime import datetime
import bcrypt

class Admin(db.Model):
    __tablename__ = 'admins'

    id            = db.Column(db.Integer, primary_key=True)
    firstname     = db.Column(db.String(50), nullable=False)
    lastname      = db.Column(db.String(50), nullable=False)
    username      = db.Column(db.String(50), unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    is_super_admin = db.Column(db.Boolean, default=False)

    # setting the password by hashing it
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    # Note:
    # hashpw(): Hashes the password using the provided salt
    # gensalt(): Generates a salt(random value)
    # encode('utf-8'): Converts the password string to bytes, which is required by bcrypt
    # decode('utf-8'): Converts the resulting hash back to a string for storage in the database

    # checking the password by comparing the hash
    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )
    
    # checkpw(): Compares the provided password (after encoding) with the stored password hash (also encoded)


    def to_dict(self):
        return {
            'id':         self.id,
            'firstname':  self.firstname,
            'lastname':   self.lastname,
            'username':   self.username,
            'email':      self.email,
            'created_at': self.created_at.isoformat(),
            'is_super_admin': self.is_super_admin
            # password_hash intentionally excluded
        }
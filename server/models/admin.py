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

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def to_dict(self):
        return {
            'id':         self.id,
            'firstname':  self.firstname,
            'lastname':   self.lastname,
            'username':   self.username,
            'email':      self.email,
            'created_at': self.created_at.isoformat(),
            # password_hash intentionally excluded
        }
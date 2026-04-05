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

if __name__ == '__main__':
    app.run(debug=True)
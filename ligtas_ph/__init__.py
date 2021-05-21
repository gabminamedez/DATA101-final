from .datastore import mmda
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'
DB_SERVER = f'sqlite:///{DB_NAME}'
DB_DATA = mmda.MMDA()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'data101baby'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    from .models import Incident,IncidentTweet,IncidentVehicles
    create_database(app)

    return app

def create_database(app):
    if not path.exists('ligtas_ph/' + DB_NAME):
        db.create_all(app=app)
        print('Database created successfully.')

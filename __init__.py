from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# looking for database
db = SQLAlchemy()
DB_NAME = "database.db"


# initiation for app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fasfaksjnfkjda'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # loading Blueprints
    from views import views
    from main import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Note

    # make a database if not exists
    create_database(app)

    # from flask_login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# if not find database let's make one 
def create_database(app):
    if not path.exists('flasknba/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

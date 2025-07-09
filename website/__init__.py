#inthis file we create the Flask app instance and register blueprints for views and auth
# This file is the entry point for the Flask application
# File: website/__init__.py
#why we use this file:
# -          To create the Flask app instance and register blueprints for views and authentication.
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialize SQLAlchemy
db = SQLAlchemy()

# Database configuration
DB_NAME = "test_db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vishal%4011@localhost:5433/test_db'  # URL-encoded password
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    # Register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Redirect to the login page if user
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
     
def create_database(app):
    with app.app_context():  # Use the application context
        db.create_all()  # Create all tables defined in models.py
        print('Database tables created successfully!')

from website import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")





#why we use this file:
# -          To define the data models for the application, such as User and Post models.
#example of a model:
# -          To create database tables and manage relationships between different data entities.

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)  # Ensure data is not nullable
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking to the User model



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Note')  # Establish a one-to-many relationship with Note model

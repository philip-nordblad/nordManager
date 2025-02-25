
from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String,nullable=False)



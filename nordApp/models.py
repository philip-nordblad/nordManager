
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
    availability = db.Column(db.JSON) # stores availability as a JSON
    shifts = db.relationship('Shift')
    role = db.Column(db.String,nullable=False)


class Shift(db.Model):

    __tablename_ = "shift"

    id = db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)



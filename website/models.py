from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    immat = db.Column(db.String(5), unique=True)
    password = db.Column(db.String(150))
    labo_name = db.Column(db.String(30))
    groupes = db.relationship('Groupe')

class Groupe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    note = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    persons = db.relationship('Person')

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cin = db.Column(db.String(8))
    fam_name = db.Column(db.String(20))
    name = db.Column(db.String(20))
    sexe = db.Column(db.String(5))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(25))
    address = db.Column(db.String(100))
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupe.id'))
from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError

class Stock_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    company = db.Column(db.Text())
    quantity = db.Column(db.Integer)
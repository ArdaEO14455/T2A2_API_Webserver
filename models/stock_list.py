from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError
# from bar import *


#Stock List Model
class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id'))

    name = db.Column(db.Text())
    type = db.Column(db.String())
    quantity = db.Column(db.Integer)

    bar_item = db.relationship('Bar', backref=db.backref('stock_list', lazy='dynamic'))
    

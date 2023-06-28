from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError
# from stock import Stock


#Bar Model
class Bar(db.Model):
    __tablename__ = 'bar_items'

    bar_id = db.Column(db.Integer, primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey('stock_items.stock_id'), nullable = False) 

    name = db.Column(db.String())
    type = db.Column(db.String())
    category = db.Column(db.String())
    quantity = db.Column(db.Integer)
    target_quantity = db.Column(db.Integer)
    bar_price = db.Column(db.Integer)

    item = db.relationship('Stock', backref=db.backref('bar_items', lazy='dynamic', cascade='save-update'))


 

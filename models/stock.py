from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Regexp
# from items import *

#Stock Model

class Stock(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False)

    name = db.Column(db.String())
    category = db.Column(db.String())
    type = db.Column(db.String())

    quantity = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)


    item = db.relationship('Item', backref=db.backref('stock_items', lazy='dynamic', cascade='save-update'))


# #Stock Schema
# class StockSchema(ma.Schema):
#     item = fields.Nested(ItemSchema)    
#     quantity = fields.Integer(required=True, validate=(Regexp('^[0-9]+$', error='Invalid quantity')))
#     class Meta:
#         fields = ('name', 'company', 'quantity', 'item_type', 'item_type_category', 'unit', 'cost_price')

from init import db, ma
from marshmallow import fields
from marshmallow.validate import Regexp
from models.items import ItemSchema


#Stock Model

class Stock(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False) #Foreign key for item_id from item table

    name = db.Column(db.String())
    category = db.Column(db.String())
    type = db.Column(db.String())

    available_stock = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)


    item_info = db.relationship('Item', backref=db.backref('stock_items', lazy='dynamic', cascade='save-update'))


#Stock Schema
class StockSchema(ma.Schema):
    # stock_id = fields.Integer(required=True)
    # name = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    item_info = fields.Nested(ItemSchema, exclude=['name'])
    available_stock = fields.Integer(required=True)
    cost_price = fields.Integer()
    
    class Meta:
        fields = ('name', 'stock_id', 'item_info' , 'available_stock', 'cost_price')
        ordered = True

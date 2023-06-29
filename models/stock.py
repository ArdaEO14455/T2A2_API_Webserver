from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Regexp
from models.items import ItemSchema

#Stock Model

class Stock(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False)

    name = db.Column(db.String())
    category = db.Column(db.String())
    type = db.Column(db.String())

    available_stock = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)


    item = db.relationship('Item', backref=db.backref('stock_items', lazy='dynamic', cascade='save-update'))


#Stock Schema
class StockSchema(ma.Schema):
    item = fields.Nested(ItemSchema, exclude=['name'])
    # name = fields.String()
    available_stock = fields.Integer(required=True)
    cost_price = fields.Integer()
    class Meta:
        fields = ('name', 'item', 'available_stock', 'cost_price')
        ordered = True

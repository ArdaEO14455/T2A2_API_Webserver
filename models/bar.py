from init import db, ma
from marshmallow import fields
from models.items import ItemSchema
from models.stock import StockSchema


#Bar Model
class Bar(db.Model):
    __tablename__ = 'bar_items'

    bar_id = db.Column(db.Integer, primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey('stock_items.stock_id'), nullable = False, unique=True) 

    name = db.Column(db.String())
    type = db.Column(db.String())
    category = db.Column(db.String())
    quantity = db.Column(db.Integer)
    target_quantity = db.Column(db.Integer) # This represents the quantities that each bar item needs to be reset
    bar_price = db.Column(db.Integer)

    bar_item = db.relationship('Stock', backref=db.backref('bar_items', lazy='dynamic', cascade='save-update'))


class BarSchema(ma.Schema):
    bar_item = fields.Nested(StockSchema, exclude=['stock_id', 'available_stock', 'cost_price'])
    quantity = fields.Integer(required=True, error='Invalid quantity')
    target_quantity = fields.Integer(required=True, error='Invalid quantity, Target Quantity must be inputted')
    
    class Meta:
        fields = ('bar_id', 'bar_item', 'quantity', 'target_quantity')
        ordered = True


from init import db, ma
from marshmallow import fields
from models.items import ItemSchema


#Stock Model

class Stock(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id', onupdate='CASCADE'), nullable = False) #Foreign key for item_id from item table

    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))

    available_stock = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)


    #item_info = db.relationship('Item', backref=db.backref('stock_items', lazy='dynamic', cascade='save-update'))
    bar_item = db.relationship('Bar', backref='stock_item', lazy=True, cascade='save-update, delete')


#Stock Schema
class StockSchema(ma.Schema):
    available_stock = fields.Integer(required=True)
    cost_price = fields.Integer()
    
    class Meta:
        fields = ('stock_id', 'name', 'category', 'type', 'available_stock', 'cost_price')
        ordered = True

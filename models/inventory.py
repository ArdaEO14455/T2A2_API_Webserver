from init import db, ma
from marshmallow import fields, validates_schema
from models.items import *

 

class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id'))

    name = db.Column(db.Text())
    company = db.Column(db.Text())
    quantity = db.Column(db.Integer)


class Bar_item(db.Model):
    __tablename__ = "bar_items"

    bar_id = db.Column(db.Integer, primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey('stock_items.stock_id', ondelete='CASCADE'), nullable=False)

    item_name = db.Column(db.Text)
    company = db.Column(db.Text)
    item_type = db.Column(db.Text()) #Wine, Beer, Spirit, Liqueur, Soft Drink
    item_type_category = db.Column(db.Text()) #Shiraz, IPA, Sauvignon Blanc
    unit = db.Column(db.Text) #CHANGE #bottle, can, keg, etc
    quantity = db.Column(db.Integer)
    max_quantity = db.Column(db.Integer)
    bar_price = db.Column(db.Integer)

class Stock_item(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id')) 

    item_name = db.relationship('Item', back_populates='name', cascade='all, delete')
    company = db.Column(db.Text())
    quantity = db.Column(db.Integer)
    item_type = db.Column(db.Text()) #Wine, Beer, Spirit, Liqueur, Soft Drink
    item_type_category = db.Column(db.Text()) #Shiraz, IPA, Sauvignon Blanc
    unit = db.Column(db.Text()) #CHANGE #bottle, can, keg, etc
    cost_price = db.Column(db.Integer)

    


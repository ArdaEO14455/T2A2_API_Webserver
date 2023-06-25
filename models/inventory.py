from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError
from models.items import *

class Stock_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey)

    name = db.Column(db.Text())
    company = db.Column(db.Text())
    quantity = db.Column(db.Integer)


class Bar_Items(db.Model):
    bar_id = db.Column(db.Integer, primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey('stock_items.id', ondelete='CASCADE'), nullable=False)

    item_name = db.Column(db.Text)
    company = db.Column(db.Text)
    item_type = db.Column(db.Text()) #Wine, Beer, Spirit, Liqueur, Soft Drink
    item_type_category = db.Column(db.Text()) #Shiraz, IPA, Sauvignon Blanc
    unit = db.Column(db.Category()) #bottle, can, keg, etc
    quantity = db.Column(db.Integer)
    max_quantity = db.Column(db.Integer)
    bar_price = db.Column(db.Integer)

class Stock_Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    company = db.Column(db.Text())
    quantity: db.Column(db.Integer)
    item_type = db.Column(db.Text()) #Wine, Beer, Spirit, Liqueur, Soft Drink
    item_type_category = db.Column(db.Text()) #Shiraz, IPA, Sauvignon Blanc
    unit = db.Column(db.Category()) #bottle, can, keg, etc
    cost_price = db.Column(db.Integer)

from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError




 

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

#Stock Model

class Stock(db.Model):
    __tablename__ = "stock_items"

    stock_id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False) 

    name = db.Column(db.String())
    type = db.Column(db.String())
    
    quantity = db.Column(db.Integer)
    cost_price = db.Column(db.Integer)


    item = db.relationship('Item', backref=db.backref('stock_items', lazy='dynamic', cascade='save-update'))




#Stock Schema
class StockSchema(ma.Schema):
    quantity = fields.Integer(required=True, validate=(Regexp('^[0-9]+$', error='Invalid quantity')))
    class Meta:
        fields = ('name', 'company', 'quantity', 'item_type', 'item_type_category', 'unit', 'cost_price')


    


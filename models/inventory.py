from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError


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




#Stock Schema
class StockSchema(ma.Schema):
    quantity = fields.Integer(required=True, validate=(Regexp('^[0-9]+$', error='Invalid quantity')))
    class Meta:
        fields = ('name', 'company', 'quantity', 'item_type', 'item_type_category', 'unit', 'cost_price')


#Bar Model
class Bar(db.Model):
    __tablename__ = 'bar_items'

    bar_id = db.Column(db.Integer, primary_key=True)

    # item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable = False) 
    stock_id = db.Column(db.Integer, db.ForeignKey('stock_items.stock_id'), nullable = False) 

    name = db.Column(db.String())
    type = db.Column(db.String())
    category = db.Column(db.String())
    quantity = db.Column(db.Integer)
    target_quantity = db.Column(db.Integer)
    bar_price = db.Column(db.Integer)

    #item = db.relationship('Item', backref=db.backref('bar_items', lazy='dynamic', cascade='save-update'))
    item = db.relationship('Stock', backref=db.backref('bar_items', lazy='dynamic', cascade='save-update'))


 

#Stock List Model
class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id'))

    name = db.Column(db.Text())
    type = db.Column(db.String())
    quantity = db.Column(db.Integer)

    bar_item = db.relationship('Bar', backref=db.backref('stock_list', lazy='dynamic'))
    



    


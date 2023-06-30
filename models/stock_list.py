from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError
# from models.items import ItemSchema
from models.items import ItemSchema


#Stock List Model
class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    stocklist_id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id'))

    name = db.Column(db.Text())
    category = db.Column(db.Text())
    type = db.Column(db.String())
    quantity_needed = db.Column(db.Integer)

    bar_item = db.relationship('Bar', backref=db.backref('stock_list', lazy='dynamic'))


class Stock_list_Schema(ma.Schema):
    name = fields.String()
    category = fields.String()
    type = fields.String()
    quantity_needed = fields.Integer(required=True)
    
    class Meta:
        fields = ('name', 'category', 'type', 'quantity_needed')
        ordered = True
    

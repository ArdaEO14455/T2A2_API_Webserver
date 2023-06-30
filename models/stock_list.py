from init import db, ma
from marshmallow import fields
from models.bar import BarSchema



#Stock List Model
class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    stocklist_id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id'))

    name = db.Column(db.Text())
    category = db.Column(db.Text())
    type = db.Column(db.String())
    quantity_needed = db.Column(db.Integer)

    stocklist_item = db.relationship('Bar', backref=db.backref('stock_list', lazy='dynamic', cascade='save-update'))


class Stock_list_Schema(ma.Schema):
    stocklist_item = fields.Nested(BarSchema, exclude=['bar_id', 'quantity', 'target_quantity' ])
    quantity_needed = fields.Integer(required=True)
    
    class Meta:
        fields = ('stocklist_id', 'stocklist_item', 'quantity_needed')
        ordered = True
    

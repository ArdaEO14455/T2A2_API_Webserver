from init import db, ma
from marshmallow import fields
from models.bar import BarSchema



#Stock List Model
class Stock_list(db.Model):
    __tablename__ = 'stock_list'

    stocklist_id = db.Column(db.Integer, primary_key=True)

    bar_id = db.Column(db.Integer, db.ForeignKey('bar_items.bar_id', onupdate='CASCADE'))

    name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))
    quantity_needed = db.Column(db.Integer)

    #stocklist_item = db.relationship('Bar', backref=db.backref('stock_list', lazy='dynamic', cascade='delete'))


class Stock_list_Schema(ma.Schema):
    quantity_needed = fields.Integer(required=True)
    
    class Meta:
        fields = ('stocklist_id', 'name', 'category', 'type', 'stocklist_item', 'quantity_needed')
        ordered = True
    

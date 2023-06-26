from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Length, OneOf, And, Regexp, ValidationError

VALID_CATEGORIES = ['Beer', 'Wine', 'Spirit']
VALID_UNITS = ['Can', 'Bottle', 'Keg']

#Beer Information

class Item:
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    name = db.relationship('Stock_Item', back_populates='item_name')
    category = db.Column(db.Text())
    type = db.Column(db.Text()) # db.relationship('Beer_type')
    company = db.Column(db.Text)
    unit = db.Column(db.Text)
    unit_volume = db.Column(db.Integer)
    alcohol_content = db.Column(db.Float)

# class ItemSchema(ma.Schema):
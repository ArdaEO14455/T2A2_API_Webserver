from init import db, ma
from models.inventory import *
from marshmallow import fields, validates_schema
from marshmallow.validate import Regexp, ValidationError


VALID_CATEGORIES = ['Beer', 'Wine', 'Spirit']
VALID_UNITS = ['Can', 'Bottle', 'Keg']

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.Text())
    category = db.Column(db.Text())
    type = db.Column(db.Text())
    company = db.Column(db.Text)
    unit = db.Column(db.Text)
    volume = db.Column(db.Integer)
    alcohol_content = db.Column(db.Float)

def add_to_stock(self, name, type, quantity, cost_price):
    stock_item = Stock(
         item=self, 
         name=name, 
         type=type, 
         quantity=quantity, 
         cost_price=cost_price)
    db.session.add(stock_item)
    db.session.commit()

def add_to_bar(self, name, type, quantity, target_quantity, bar_price):
    bar_items = Bar(
         item=self, 
         name=name, 
         type=type, 
         quantity=quantity,
         target_quantity=target_quantity, 
         bar_price=bar_price)
    db.session.add(bar_items)
    db.session.commit()

class ItemSchema(ma.Schema):
    name = fields.String(required=True, validate=(Regexp('^[a-zA-Z0-9]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    type = fields.String(required=True)
    company = fields.String(required=True)
    volume = fields.Integer

    @validates_schema()
    def validate_category(self, data, **kwargs):
            category = [x for x in VALID_CATEGORIES if x.upper() == data['category'].upper()]
            if len(category) == 0:
                 raise ValidationError(f'Category must be filled in with one of: {VALID_CATEGORIES}')
            data['category'] = category [0]
    def validate_units(self, data, **kwargs):
            unit = [x for x in VALID_UNITS if x.upper() == data['unit'].upper()]
            if len(unit) == 0:
                 raise ValidationError(f'Invalid Unit, must be one of the following: {VALID_CATEGORIES}')
            data['unit'] = unit[0]

class Meta:
    fields = ('id', 'name', 'category', 'type', 'company', 'unit', 'volume', 'alcohol_content')
    ordered = True


from init import db, ma
# from models.inventory import *
from marshmallow import fields, validates_schema, validates
from marshmallow.validate import Regexp, ValidationError, OneOf


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
    alcohol_content = db.Column(db.String)


class ItemSchema(ma.Schema):
    name = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    category = fields.String(load_default=(VALID_CATEGORIES[0]))
    type = fields.String()
    company = fields.String()
    unit = fields.String(validate=Regexp)
    volume = fields.Integer()
    alcohol_content = fields.String(validate=(Regexp('^[0-9%]+$')))


    @validates_schema
    def validate_category(self, data, **kwargs):
            
            category = [x for x in VALID_CATEGORIES if x.upper() == data['category'].upper()]
            if len(category) == 0:
                 raise ValidationError(f'Category must be filled in with one of: {VALID_CATEGORIES}')
            data['category'] = category[0]

    @validates_schema
    def validate_units(self, data, **kwargs):
            
            unit = [x for x in VALID_UNITS if x.upper() == data['unit'].upper()]
            if len(unit) == 0:
                 raise ValidationError(f'Invalid Unit, must be one of the following: {VALID_CATEGORIES}')
            data['unit'] = unit[0]

    @validates_schema
    def validate_alcohol_content(self, data, **kwargs):
    
        alcohol_content = data['alcohol_content']
        if alcohol_content is not None:
            # Append '%' symbol to the value
            if not isinstance(alcohol_content, str):
                alcohol_content = str(alcohol_content)
            if not alcohol_content.endswith('%'):
                alcohol_content += '%'
            
            data['alcohol_content'] = alcohol_content

    class Meta:
        fields = ('name', 'category', 'type', 'company', 'unit', 'volume', 'alcohol_content')
        ordered = True


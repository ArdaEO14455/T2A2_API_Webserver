from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Regexp, ValidationError


VALID_CATEGORIES = ['Beer', 'Wine', 'Spirit']
VALID_UNITS = ['Can', 'Bottle', 'Keg']

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(), unique=True)
    category = db.Column(db.String())
    type = db.Column(db.String())
    company = db.Column(db.String())
    unit = db.Column(db.String())
    volume = db.Column(db.Integer)


class ItemSchema(ma.Schema):
    name = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    category = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    type = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    company = fields.String()
    unit = fields.String()
    volume = fields.Integer()


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
    def validate_category(self, data, **kwargs):
            
            category = [x for x in VALID_CATEGORIES if x.upper() == data['category'].upper()]
            if len(category) == 0:
                 raise ValidationError(f'Category must be filled in with one of: {VALID_CATEGORIES}')
            data['category'] = category[0]
    

    class Meta:
        fields = ('name', 'category', 'type', 'company', 'unit', 'volume', 'alcohol_content')
        ordered = True


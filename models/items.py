from init import db, ma
from marshmallow import fields, validates_schema
from marshmallow.validate import Regexp, ValidationError


VALID_CATEGORIES = ['Other', 'Beer', 'Wine', 'Spirit']
VALID_UNITS = ['Other', 'Can', 'Bottle', 'Keg']

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), unique=True, nullable = False)
    category = db.Column(db.String(50)) #Beer, Wine, Spirit as basic categories. Also distinction is necessary for cli_commands for example stock generation & testing functionality
    type = db.Column(db.String(50)) #sub-category of the above category - Pale ale, Pinot Noir, etc.
    company = db.Column(db.String(50))
    unit = db.Column(db.String(50)) #Distinguish container for stock item, as distinguishing between a can of beer and a keg is important
    volume = db.Column(db.Integer) #Fluff parameter to add some additional information, not crucial for functionality

    stock_items = db.relationship('Stock', backref='item', lazy=True, cascade='save-update, delete')
    
class ItemSchema(ma.Schema):
    name = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    category = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    type = fields.String(required=True, validate=(Regexp('^[a-zA-Z\s]+$', error='Special Characters (#,$,@ etc) are not allowed')))
    company = fields.String()
    unit = fields.String(load_default=VALID_UNITS[0])
    volume = fields.Integer()


    @validates_schema
    def validate_category(self, data, **kwargs): #Validate Category
            
            category = [x for x in VALID_CATEGORIES if x.upper() == data['category'].upper()]
            if len(category) == 0:
                 raise ValidationError(f'Category must be filled in with one of: {VALID_CATEGORIES}')
            data['category'] = category[0]

    @validates_schema
    def validate_units(self, data, **kwargs): #Validate Unit Input
            
            unit = [x for x in VALID_UNITS if x.upper() == data['unit'].upper()]
            if len(unit) == 0:
                 raise ValidationError(f'Invalid Unit, must be one of the following: {VALID_CATEGORIES}')
            data['unit'] = unit[0]
    
    class Meta:
        fields = ('id', 'name', 'category', 'type', 'company', 'unit', 'volume', 'alcohol_content')
        ordered = True


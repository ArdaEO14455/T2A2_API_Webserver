from init import db, ma


#General Information

class Unit:
    __tablename__ = 'units'

    unit_id = db.Column(db.Integer, primary_key=True)

    unit_name = db.Column(db.Text())

    unit_volume_ml = db.column(db.Integer)


class Company:
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.Text())


#Beer Information

class Beer_type:
    __tablename__ = 'beer_types'

    beer_type_id = db.Column(db.Integer, primary_key=True)
    beer_type = db.Column(db.Text())


class Beer:
    __tablename__ = 'beers'

    beer_id = db.Column(db.Integer, primary_key=True)

    beer_name = db.Column(db.Text())

    #Backfilled Information
    beer_type_id = db.Column(db.Integer, db.ForeignKey('beer_types.beer_type_id'), nullable=False)
    type = db.Column(db.relationship('Beer_type'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    company = db.Column(db.relationship('Company'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    unit = db.Column(db.relationship('Unit', back_populates='beer_units', uselist=True))
    alcohol_content = beer_id = db.Column(db.FLoat)

    

#Wine Information

class Wine_Type:
    __tablename__ = 'wine_types'

    wine_type_id = db.Column(db.Integer, primary_key=True)
    wine_type_name = db.Column(db.Text())

class Wine:
    __tablename__ = 'wines'

    wine_id = db.Column(db.Integer, primary_key=True)
    wine_name = db.Column(db.Text())

    #Backfilled Information
    wine_type_id = db.Column(db.Integer, db.ForeignKey('wine_types.wine_type_id'), nullable=False)
    type = db.Column(db.relationship('Wine_type'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    company = db.Column(db.relationship('Company'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    unit = db.Column(db.relationship('Unit', back_populates='wine_units', uselist=True))
    alcohol_content = beer_id = db.Column(db.Float)
    

#Spirit Information
class Spirit_type:
    __tablename__ = 'spirit_types'

    spirit_type_id = db.Column(db.Integer, primary_key=True)
    spirit_type_name = db.Column(db.Text())

class Spirit:
    __tablename__ = 'spirits'

    spirit_id = db.Column(db.Integer, primary_key=True)
    spirit_name = db.Column(db.Text())

    #Backfilled Information
    spirit_type_id = db.Column(db.Integer, db.ForeignKey('spirit_types.spirit_type_id'), nullable=False)
    type = db.Column(db.relationship('Spirit_type'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    company = db.Column(db.relationship('Company'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'), nullable=False)
    unit = db.Column(db.relationship('Unit', back_populates='spirit_units', uselist=True))
    alcohol_content = beer_id = db.Column(db.Float)

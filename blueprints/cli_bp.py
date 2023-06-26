from flask import Blueprint
from init import db
from models.inventory import *
from models.items import *

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Stock Tables Created Successfully')

@cli_bp.cli.command('clear')
def clear_db():
    db.drop_all()

@cli_bp.cli.command('create_inventory')
def create_inventory():
    stock = [
        Stock_item(
            item_name="nectar",
            company="WTB",
            quantity=5 ,
            item_type="beer" ,
            item_type_category="NEIPA" ,
            unit="can",
            cost_price=5
        ),
        Stock_item(
            item_name = 'Nectar of the Hops',
            company = 'Willie the Boatman',
            quantity = 4,
            item_type =  'Beer',
            item_type_category = 'New England IPA',
            unit = 'Keg',
            cost_price = 400
        ),
        Stock_item(
            item_name = 'Pash The Magic Dragon',
            company = 'Batch Brewing Company',
            quantity = 40,
            item_type =  'Beer',
            item_type_category = 'Sour Beer',
            unit = 'can',
            cost_price = 5.80
        )
]

    db.session.query(Stock_item).delete()
    db.session.add_all(stock)
    db.session.commit()

    # bar = [
    #     Bar_item(
            
    #     )

    # ]

    # db.session.query(Bar_Items).delete()
    # db.session.add_all(bar)
    # db.session.commit()

    print("Inventory Created")
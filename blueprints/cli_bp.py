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
    # items = [
    #     Item(
    #         name="nectar",
    #         category = 'Beer',
    #         type="NEIPA" ,
    #         company="WTB",
    #         unit = 'Can'
    #     ),
    #     Item (
    #         name='Nectar of the Hops',
    #         category = 'Beer',
    #         type='New England IPA' ,
    #         company='Willie the Boatman',
    #         unit = 'Keg'
    #     ),
    #     Item(
    #         name='Pash The Magic Dragon',
    #         category = 'Beer',
    #         type='Sour Beer',
    #         company='Batch Brewing Company',
    #         unit = 'Can'
    #     )
    # ]
    stock = [
        Stock(
            name="nectar",
            company="WTB",
            quantity=5 ,
            item_type="Beer" ,
            item_type_category="NEIPA" ,
            unit="Can",
            cost_price=5
        ),
        # Stock(
        #     name = 'Nectar of the Hops',
        #     company = 'Willie the Boatman',
        #     quantity = 4,
        #     item_type =  'Beer',
        #     item_type_category = 'New England IPA',
        #     unit = 'Keg',
        #     cost_price = 400
        # ),
        # Stock(
        #     name = 'Pash The Magic Dragon',
        #     company = 'Batch Brewing Company',
        #     quantity = 40,
        #     item_type = 'Beer',
        #     item_type_category = 'Sour Beer',
        #     unit = 'Can',
        #     cost_price = 5.80
        # )
]

    db.session.query(Stock).delete()
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


@cli_bp.cli.command('create_item')
def create_db():
    item = Item(
        name='Pash',
        category='Beer', 
        type='Sour', 
        company='coca-cola', 
        unit='bottle', 
        volume=500, 
        alcohol_content=0
    )
    add_to_stock(item, quantity=10, cost_price=50)
    print('Item Added')


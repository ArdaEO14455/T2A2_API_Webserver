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
]

    db.session.query(Stock).delete()
    db.session.add_all(stock)
    db.session.commit()

    print("Inventory Created")


@cli_bp.cli.command('create_stock_A')
def create_inventory():
    item = Item(
        name='Pash',
        category='Beer', 
        type='Sour', 
        company='Batch Brewing Company', 
        unit='can', 
        volume=375, 
        alcohol_content=4
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=60, cost_price=5)

    item = Item(
        name='Nectar',
        category='Beer', 
        type='NEIPA', 
        company='WTB', 
        unit='can', 
        volume=375, 
        alcohol_content=5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=60, cost_price=5)

    item = Item(
        name='Pink Gallah',
        category='Beer', 
        type='Pink Lemonade Sour Ale', 
        company='Grifter Brewery', 
        unit='can', 
        volume=375, 
        alcohol_content=5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=60, cost_price=5)

    item = Item(
        name='Little Giant',
        category='Wine', 
        type='Shiraz', 
        company='Unknown', 
        unit='Bottle', 
        volume=500, 
        alcohol_content=14
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=25)

    item = Item(
        name='Sagitarious',
        category='Wine', 
        type='Cabernet Sauvignon', 
        company='Twelve Signs', 
        unit='Bottle', 
        volume=500, 
        alcohol_content=14
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=16)

    item = Item(
        name='Break Free',
        category='Wine', 
        type='Skin-On Rose', 
        company='Unknown', 
        unit='Bottle', 
        volume=500, 
        alcohol_content=14
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=20)

    item = Item(
        name='Smirnoff Vodka',
        category='Spirit', 
        type='Vodka', 
        company='Smirnoff', 
        unit='Bottle', 
        volume=1000, 
        alcohol_content=37.5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=20)

    item = Item(
        name='Poor Toms Strawberry Gin',
        category='Spirit', 
        type='Gin', 
        company='Poor Toms', 
        unit='Bottle', 
        volume=1000, 
        alcohol_content=37.5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=20)

    item = Item(
        name='Bloody Shiraz Gin',
        category='Spirit', 
        type='Gin', 
        company='Four Pillars', 
        unit='Bottle', 
        volume=1000, 
        alcohol_content=37.5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=20)

    print('Example Stock Created')


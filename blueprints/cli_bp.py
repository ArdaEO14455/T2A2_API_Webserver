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
    print('All Tables Dropped')

@cli_bp.cli.command('generate_stock')
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
    add_to_bar(item, name=item.name, type=item.type, quantity=8, target_quantity=10, bar_price=9)

    item = Item(
        name='Nectar',
        category='Beer', 
        type='NEIPA', 
        company='WTB', 
        unit='Keg', 
        volume=4000, 
        alcohol_content=5
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=5, cost_price=350)
    add_to_bar(item, name=item.name, type=item.type, quantity=2, target_quantity=4, bar_price=0)

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
    add_to_bar(item, name=item.name, type=item.type, quantity=8, target_quantity=10, bar_price=0)


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
    add_to_bar(item, name=item.name, type=item.type, quantity=10, target_quantity=12, bar_price=50)


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
    add_to_bar(item, name=item.name, type=item.type, quantity=10, target_quantity=12, bar_price=55)


    item = Item(
        name='Break Free',
        category='Wine', 
        type='Skin-On Rose', 
        company='Unknown', 
        unit='Bottle', 
        volume=500, 
        alcohol_content=14
    )
    add_to_stock(item, name=item.name, type=item.type, quantity=20, cost_price=60)
    add_to_bar(item, name=item.name, type=item.type, quantity=8, target_quantity=10, bar_price=45)


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
    add_to_bar(item, name=item.name, type=item.type, quantity=2, target_quantity=4, bar_price=0)

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
    add_to_bar(item, name=item.name, type=item.type, quantity=1, target_quantity=4, bar_price=0)

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
    add_to_bar(item, name=item.name, type=item.type, quantity=4, target_quantity=4, bar_price=0)

    print('Example Stock Created')

@cli_bp.cli.command('stock_list')
def create_stocklist():
    bar_items = db.session.query(Bar).all()
    for item in bar_items:
        stock_item = Stock_list.query.filter_by(name=item.name, type=item.type).first()
        if stock_item is None:
            stock_item = Stock_list(
            bar_item= item,
            name= item.name,
            type = item.type,
            quantity= (item.target_quantity - item.quantity)
            )
        if stock_item.quantity > 0:
                
                db.session.close()
                db.session.add(stock_item)
                db.session.commit()

                #add_to_stocklist(stock_item.bar_item, name=stock_item.name, type=stock_item.type, quantity=stock_item.quantity)
    print('Stocklist Created')

from flask import Blueprint
from init import db
from models.items import Item
from models.stock import Stock
from models.bar import Bar
from models.stock_list import Stock_list


cli_bp = Blueprint('db', __name__)

#create database

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Stock Tables Created Successfully')

@cli_bp.cli.command('clear')
def clear_db():
    db.drop_all()
    print('All Tables Dropped')

#generate placeholder items

@cli_bp.cli.command('generate_items')
def create_inventory():
    items = [
    Item(
        name='Pash',
        category='Beer', 
        type='Sour', 
        company='Batch Brewing Company', 
        unit='Can', 
        volume=375 
    ),
    Item(
        name='Nectar of the Hops',
        category='Beer', 
        type='NEIPA', 
        company='WTB', 
        unit='Keg', 
        volume=4000 
    ),
    Item(
        name='Pink Gallah',
        category='Beer', 
        type='Pink Lemonade Sour Ale', 
        company='Grifter Brewery', 
        unit='Can', 
        volume=375 
    ),
    Item(
        name='Little Giant',
        category='Wine', 
        type='Shiraz', 
        company='Unknown', 
        unit='Bottle', 
        volume=500
    ),
    Item(
        name='Sagitarious',
        category='Wine', 
        type='Cabernet Sauvignon', 
        company='Twelve Signs', 
        unit='Bottle', 
        volume=500
    ),
    Item(
        name='Break Free',
        category='Wine', 
        type='Skin-On Rose', 
        company='Unknown', 
        unit='Bottle', 
        volume=500 
    ),
    Item(
        name='Smirnoff Vodka',
        category='Spirit', 
        type='Vodka', 
        company='Smirnoff', 
        unit='Bottle', 
        volume=1000 
    ),
    Item(
        name='Poor Toms Strawberry Gin',
        category='Spirit', 
        type='Gin', 
        company='Poor Toms', 
        unit='Bottle', 
        volume=1000 
    ),
    Item(
        name='Bloody Shiraz Gin',
        category='Spirit', 
        type='Gin', 
        company='Four Pillars', 
        unit='Bottle', 
        volume=1000 
    )
    ]
    db.session.query(Item).delete()
    db.session.add_all(items)
    db.session.commit()
    
    print('Items Generated')

#add items from items table to stock table

@cli_bp.cli.command('add_stock')
def add_to_stock():
    items = db.session.query(Item).all() #Query the Bar table and iterate over rows
    for item in items: 
        stock_item = Stock.query.filter_by(name=item.name, type=item.type).first() #check to see if the item is already in the stock table
        if stock_item is None:
            stock_item = Stock(
            info = item,
            name = item.name,
            category = item.category,
            type = item.type,
            available_stock = 20,
            cost_price = 0
            )
        db.session.add(stock_item)
        db.session.commit()

    print('Added items to Stock')

#add items in stock to bar inventory

@cli_bp.cli.command('bar_inventory')
def create_bar_inventory():
    stock_items = db.session.query(Stock).all()
    for stock_item in stock_items: 
        bar_item = Bar.query.filter_by(name=stock_item.name, type=stock_item.type).first() #check to see if the item is already in the stock table
        if bar_item is None:
            if stock_item.category == 'Wine':
                bar_item = Bar(
                    item = stock_item,
                    name= stock_item.name,
                    category = stock_item.category,
                    type = stock_item.type,
                    quantity = 10,
                    target_quantity = 12,
                    bar_price = 50,
                )
            elif stock_item.category == 'Beer':
                bar_item = Bar(
                item = stock_item,
                name= stock_item.name,
                category = stock_item.category,
                type = stock_item.type,
                quantity = 18,
                target_quantity = 20,
                bar_price = 10,
                )
            elif stock_item.category == 'Spirit':
                bar_item = Bar(
                item = stock_item,
                name= stock_item.name,
                category = stock_item.category,
                type = stock_item.type,
                quantity = 2,
                target_quantity = 4,
                bar_price = 0
                )
            
        db.session.add(bar_item)
        db.session.commit()

    print('Bar Inventory Added')

#Create Stocklist Command

@cli_bp.cli.command('stock_list')
def create_stocklist():
    bar_items = db.session.query(Bar).all() #Query the Bar table and iterate over rows
    for item in bar_items: 
        stock_item = Stock_list.query.filter_by(name=item.name, type=item.type).first() #check to see if the item is already in the stock table
        if stock_item is None:
            stock_item = Stock_list(
            bar_item = item,
            category = item.category,
            name= item.name,
            type = item.type,
            quantity_needed= (item.target_quantity - item.quantity) #determine how many of each item is needed to reach target quantity
            )
        if stock_item.quantity_needed > 0:
                
                db.session.close()
                db.session.add(stock_item)
                db.session.commit()

                #add_to_stocklist(stock_item.bar_item, name=stock_item.name, type=stock_item.type, quantity=stock_item.quantity)
    print('Stocklist Created')

#Commit Stocktake & Update Bar & Stock Quantities
@cli_bp.cli.command('commit_stocktake')
def commit_stocktake():
    stock_list_items = db.session.query(Stock_list).all() #Query the Stock_List table and iterate over the items
    for stock_list_item in stock_list_items:
        bar_item = Bar.query.filter_by(name=stock_list_item.name).first() #Query Bar table for matching stock-list items based on matching name
        bar_item.quantity += stock_list_item.quantity_needed #Add stock-list item quantity to matching bar item quantity

        stock_item = Stock.query.filter_by(name=stock_list_item.name).first() #Query Stock table for matching stock-list items based on matching stock ID
        stock_item.quantity -= stock_list_item.quantity_needed #Subtract stock-list item quantity from matching stock item quantity based on name
    
    db.session.commit()
    print('Stocktake Completed, Stock Updated')


# @cli_bp.cli.command('test_all')
# def test_all():
#     create_db()
#     create_inventory()
#     add_to_stock()
#     create_bar_inventory()
#     create_stocklist()
    

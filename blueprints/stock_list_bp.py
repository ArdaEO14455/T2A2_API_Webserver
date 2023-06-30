from flask import Blueprint, request, jsonify
from init import db
from models.stock_list import Stock_list, Stock_list_Schema
from models.bar import Bar, BarSchema
from models.stock import Stock
from psycopg2 import IntegrityError




stocklist_bp = Blueprint('stocklist', __name__, url_prefix='/stocklist')

@stocklist_bp.route('/')
def view_stocklist():
    stmt = db.Select(Stock_list).order_by(Stock_list.quantity_needed.desc())
    stock_list = db.session.scalars(stmt).all()
    return Stock_list_Schema(many=True).dumps(stock_list)

@stocklist_bp.route('/<int:stocklist_id>', methods=['POST'])
def add_to_stock_list(stocklist_id):
    try:
        stock_list_details = Stock_list_Schema().load(request.json)
        stmt = db.select(Bar).filter_by(bar_id=stocklist_id)
        bar_item = db.session.scalar(stmt)

        # # Check if an item with the same name already exists
        existing_item = Bar.query.filter_by(bar_id=bar_item.item.id).first()
        if existing_item:
          raise ValueError
        
        if bar_item:
            # Create a new Bar instance
            stock_list_item = Stock_list(
                #most item information is back-filled
                bar_id = bar_item.bar_id,
                name = bar_item.name,
                category = bar_item.category,
                type = bar_item.type,

                #available stock and its cost price need to be added individually
                quantity_needed = stock_list_details['quantity_needed'],
      
            )
            
            # Add and commit the new stock to the session
            db.session.add(stock_list_item)
            db.session.commit()
            
            return Stock_list_Schema().dump(stock_list_item), 201
        else:
            return jsonify({'error': 'Item not found'}), 404
    except:
        IntegrityError
        return jsonify({'error': 'bar item with that name already exists'}), 409 #Resource already exists 


# #Find an item:
@stocklist_bp.route('/<int:stocklist_id>', methods=['GET'])
def bar_item(stocklist_id):
  stmt = db.select(Stock_list).filter_by(stocklist_id=stocklist_id)
  stocklist_item = db.session.scalar(stmt)
  if bar_item:
    return Stock_list_Schema().dumps(stocklist_item)
  else:
    return {'error': 'Bar Item not found'}, 404

# #Delete an item:
@stocklist_bp.route('/<int:bar_id>', methods=['DELETE'])
def delete_item(stocklist_id):
    stmt = db.select(Stock_list).filter_by(bar_id=stocklist_id)
    stocklist_item = db.session.scalar(stmt)
    if stocklist_item:
        db.session.delete(stocklist_item)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Bar Item does not exist'}, 404


#Update an item
@stocklist_bp.route('/<int:stocklist_id>', methods=['PATCH'])
def update_item(stocklist_id):
  stmt = db.select(Stock_list).filter_by(stocklist_id=stocklist_id)
  stocklist_item = db.session.scalar(stmt)
  stocklist_item_info = Stock_list_Schema().load(request.json)
  if stocklist_item:
    stocklist_item.quantity = stocklist_item_info.get('quantity', stocklist_item.quantity)
    stocklist_item.target_quantity = stocklist_item_info.get('target_quantity', stocklist_item.target_quantity)
    
    db.session.commit()
    return BarSchema().dump(bar_item)
  else:
    return {'error': 'item not found'}, 404
  

#Create Stocklist Function

@stocklist_bp.route('/create', methods=['POST'])
def create_stocklist():
    Stock_list.query.delete()
    db.session.commit()
    bar_items = db.session.query(Bar).all() #Query the Bar table and iterate over rows
    for item in bar_items: 
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

    
    stmt = db.Select(Stock_list).order_by(Stock_list.quantity_needed.desc())
    stock_list = db.session.scalars(stmt).all()
    return Stock_list_Schema(many=True).dumps(stock_list), 200

#Commit Stocktake & Update Bar & Stock Quantities
@stocklist_bp.route('/commit', methods=['PATCH'])
def commit_stocktake():
    stock_list_items = db.session.query(Stock_list).all() #Query the Stock_List table and iterate over the items
    for stock_list_item in stock_list_items:
        bar_item = Bar.query.filter_by(name=stock_list_item.name).first() #Query Bar table for matching stock-list items based on matching name
        bar_item.quantity += stock_list_item.quantity_needed #Add stock-list item quantity to matching bar item quantity

        stock_item = Stock.query.filter_by(name=stock_list_item.name).first() #Query Stock table for matching stock-list items based on matching stock ID
        stock_item.available_stock -= stock_list_item.quantity_needed #Subtract stock-list item quantity from matching stock item quantity based on name
        db.session.commit()
    Stock_list.query.delete()
    db.session.commit()
    return ('Stocktake Completed, Stock Updated')
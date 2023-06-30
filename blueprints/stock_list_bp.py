from flask import Blueprint, request, jsonify
from init import db
from models.stock_list import Stock_list, Stock_list_Schema
from models.bar import Bar, BarSchema
from psycopg2 import IntegrityError




stocklist_bp = Blueprint('stocklist', __name__, url_prefix='/stocklist')

@stocklist_bp.route('/')
def view_stocklist():
    stmt = db.Select(Stock_list).order_by(Stock_list.quantity_needed.desc())
    stock_list = db.session.scalars(stmt).all()
    return Stock_list_Schema(many=True).dumps(stock_list)

@stocklist_bp.route('/<int:id>', methods=['POST'])
def add_to_stock_list(id):
    # try:
        stock_list_details = Stock_list_Schema().load(request.json)
        stmt = db.select(Bar).filter_by(bar_id=id)
        bar_item = db.session.scalar(stmt)
        
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
    # except:
    #     IntegrityError
    #     return jsonify({'error': 'bar item with that name already exists'}), 409 #Resource already exists 


# #Find an item:
@stocklist_bp.route('/<int:bar_id>', methods=['GET'])
def bar_item(bar_id):
  stmt = db.select(Bar).filter_by(bar_id=bar_id)
  bar_item = db.session.scalar(stmt)
  if bar_item:
    return BarSchema().dump(bar_item)
  else:
    return {'error': 'Bar Item not found'}, 404

# #Delete an item:
@stocklist_bp.route('/<int:bar_id>', methods=['Delete'])
def delete_item(bar_id):
    stmt = db.select(Bar).filter_by(bar_id=bar_id)
    bar_item = db.session.scalar(stmt)
    if bar_item:
        db.session.delete(bar_item)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Bar Item does not exist'}, 404


#Update an item
@stocklist_bp.route('/<int:bar_id>', methods=['PATCH'])
def update_item(bar_id):
  stmt = db.select(Bar).filter_by(bar_id=bar_id)
  bar_item = db.session.scalar(stmt)
  bar_item_info = BarSchema().load(request.json)
  if bar_item:
    bar_item.quantity = bar_item_info.get('quantity', bar_item.quantity)
    bar_item.target_quantity = bar_item_info.get('target_quantity', bar_item.target_quantity)
    
    db.session.commit()
    return BarSchema().dump(bar_item)
  else:
    return {'error': 'item not found'}, 404
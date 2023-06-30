from flask import Blueprint, request, jsonify
from init import db
from models.bar import Bar, BarSchema
from models.stock import Stock, StockSchema
from psycopg2 import IntegrityError



bar_bp = Blueprint('bar', __name__, url_prefix='/bar')

@bar_bp.route('/')
def bar():
    stmt = db.Select(Bar).order_by(Bar.quantity.desc())
    bar = db.session.scalars(stmt).all()
    return BarSchema(many=True).dumps(bar)

#Add item from stock table to the bar table
@bar_bp.route('/<int:id>', methods=['POST'])
def add_to_bar(id):
    try:
        bar_item_details = BarSchema().load(request.json)
        stmt = db.select(Stock).filter_by(stock_id=id)
        stock_item = db.session.scalar(stmt)
        
        if stock_item:
            # Create a new Bar instance
            bar_item = Bar(
                #most item information is back-filled
                stock_id = stock_item.stock_id,
                name = stock_item.name,
                category = stock_item.category,
                type = stock_item.type,

                #available stock and its cost price need to be added individually
                quantity = bar_item_details['quantity'],
                target_quantity = bar_item_details['target_quantity']
                
            )
            
            # Add and commit the new stock to the session
            db.session.add(bar_item)
            db.session.commit()
            
            return BarSchema().dumps(bar_item), 201
        else:
            return jsonify({'error': 'Item not found'}), 404
    except:
        IntegrityError
        return jsonify({'error': 'bar item with that name already exists'}), 409 #Resource already exists 


# #Find an item:
@bar_bp.route('/<int:bar_id>', methods=['GET'])
def bar_item(bar_id):
  stmt = db.select(Bar).filter_by(bar_id=bar_id)
  bar_item = db.session.scalar(stmt)
  if bar_item:
    return BarSchema().dump(bar_item)
  else:
    return {'error': 'Bar Item not found'}, 404

# #Delete an item:
@bar_bp.route('/<int:bar_id>', methods=['Delete'])
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
@bar_bp.route('/<int:bar_id>', methods=['PATCH'])
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


from flask import Blueprint, request, jsonify
from init import db
from models.stock import Stock, StockSchema
from models.items import Item, ItemSchema
from psycopg2 import IntegrityError

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# @cli_bp.route('/')
# def index():
#     return 'Hello, Welcome to Stock Management! Here you can manually manage your stock based on quantities'

@stock_bp.route('/')
def stock():
    stmt = db.Select(Stock).order_by(Stock.category.desc())
    stock = db.session.scalars(stmt).all()
    return StockSchema(many=True).dumps(stock)

@stock_bp.route('/add', methods=['POST'])
def add_to_stock():
    try:
        item_details = StockSchema().load(request.json)
        
        # Retrieve the item from the database by name
        item = db.session.query(Item).filter_by(name=item_details['name']).first()
        
        if item:
            # Create a new stock instance
            stock = Stock(
                #most item information is back-filled
                item_id = item.id,
                name = item.name,
                category = item.category,
                type = item.type,

                #available stock and its cost price need to be added individually
                available_stock = item_details['available_stock'],
                cost_price = item_details['cost_price']
            )
            
            # Add and commit the new stock to the session
            db.session.add(stock)
            db.session.commit()
            
            return StockSchema().dump(stock), 201
        else:
            return jsonify({'error': 'Item not found'}), 404
    except:
        IntegrityError
        return jsonify({'error': 'stock item with that name already exists'}), 409 #Resource already exists 

#Example Input:
#{
#     "name": "Little Giant",
#     "available_stock": 20,
#     "cost_price": 20
#}


#Find an item:
@stock_bp.route('/<int:stock_id>', methods=['GET'])
def stock_item(stock_id):
  stmt = db.select(Stock).filter_by(stock_id=stock_id)
  item = db.session.scalar(stmt)
  if item:
    return StockSchema().dump(item)
  else:
    return {'error': 'Card not found'}, 404

#Delete an item:
@stock_bp.route('/<int:stock_id>', methods=['Delete'])
def delete_item(stock_id):
    stmt = db.select(Stock).filter_by(stock_id=stock_id)
    item = db.session.scalar(stmt)
    if item:
        db.session.delete(item)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Item does not exist'}, 404


#Update an item
@stock_bp.route('/<int:stock_id>', methods=['PATCH'])
def update_item(stock_id):
  stmt = db.select(Stock).filter_by(stock_id=stock_id)
  item = db.session.scalar(stmt)
  item_info = StockSchema().load(request.json)
  if item:
    item.name = item_info.get('name', item.name)
    item.available_stock = item_info.get('available_stock', item.available_stock)
    item.cost_price = item_info.get('cost_price', item.cost_price)
    
    db.session.commit()
    return StockSchema().dump(item)
  else:
    return {'error': 'item not found'}, 404

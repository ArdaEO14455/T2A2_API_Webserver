from flask import Blueprint, request, jsonify
from init import db
from models.stock import Stock, StockSchema
from models.items import Item, ItemSchema


stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

#See all Stock Items
@stock_bp.route('/')
def stock():
    stmt = db.Select(Stock).order_by(Stock.category.desc())
    stock = db.session.scalars(stmt).all()
    return StockSchema(many=True).dumps(stock)


#Add Stock item from Item Table based on Item ID
@stock_bp.route('/<int:id>', methods=['POST'])
def add_to_stock(id):
  try:
      stock_item_details = StockSchema().load(request.json)
      stmt = db.select(Item).filter_by(id=id)
      item = db.session.scalar(stmt)

      # # Check if an item with the same name already exists
      existing_item = Stock.query.filter_by(item_id=item.id).first()
      if existing_item:
          raise ValueError
      
      if item:
          # Create a new stock instance
          stock = Stock(
              #most item information is back-filled
              item_id = item.id,
              name = item.name,
              category = item.category,
              type = item.type,

              #available stock and its cost price need to be added individually in Json format
              available_stock = stock_item_details['available_stock'],
              cost_price =stock_item_details['cost_price']
          )
          
          # Add and commit the new stock to the session
          db.session.add(stock)
          db.session.commit()
          
          return StockSchema().dump(stock), 201
      else:
          return jsonify({'error': 'Item not found'}), 404
  except:
      ValueError
      return jsonify({'error': 'stock item with that item ID already exists'}), 409 #Resource already exists 

#Example:
#Remember to add the item Id to the URL first, e.g.: localhost:5000/stock/4
#JSON input:
#{ 
#     "available_stock": 20,
#     "cost_price": 20
#}


#Find an item:
@stock_bp.route('/<int:stock_id>', methods=['GET'])
def stock_item(stock_id):
  stmt = db.select(Stock).filter_by(stock_id=stock_id)
  stock_item = db.session.scalar(stmt)
  if stock_item:
    return StockSchema().dump(stock_item)
  else:
    return {'error': 'Card not found'}, 404

#Delete an item:
@stock_bp.route('/<int:stock_id>', methods=['Delete'])
def delete_item(stock_id):
    stmt = db.select(Stock).filter_by(stock_id=stock_id)
    stock_item = db.session.scalar(stmt)
    if stock_item:
        db.session.delete(stock_item)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Item does not exist'}, 404


#Update an item
@stock_bp.route('/<int:stock_id>', methods=['PATCH'])
def update_item(stock_id):
  stmt = db.select(Stock).filter_by(stock_id=stock_id)
  stock_item = db.session.scalar(stmt)
  stock_item_info = StockSchema().load(request.json)
  if stock_item:
    stock_item.name = stock_item_info.get('name', stock_item.name)
    stock_item.available_stock = stock_item_info.get('available_stock', stock_item.available_stock)
    stock_item.cost_price = stock_item_info.get('cost_price', stock_item.cost_price)
    
    db.session.commit()
    return StockSchema().dump(stock_item)
  else:
    return {'error': 'item not found'}, 404


#Clear Stock Table
@stock_bp.route('/clear', methods=['DELETE'])
def clear_table():
   Stock.query.delete()
   db.session.commit()
   return{}, 200
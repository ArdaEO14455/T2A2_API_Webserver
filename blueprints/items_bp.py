from flask import Blueprint, request
from models.items import *
from models.stock import *

items_bp = Blueprint('items', __name__, url_prefix='/items')


@items_bp.route('/', methods=['GET'])
def items():
    stmt = db.Select(Item).order_by(Item.category.desc())
    item = db.session.scalars(stmt).all()
    if item:
        return ItemSchema(many=True).dumps(item)
    else:
        return {'error': 'No items found'}, 404

#Create an Item
@items_bp.route('/', methods=['POST'])
def add_stock():
    try:
        #Load POST data via the Schema
        item_details = ItemSchema().load(request.json)

        # Check if an item with the same name already exists
        existing_item = Item.query.filter_by(name=item_details['name']).first()
        if existing_item:
            raise ValueError
        #Create new item instance
        item = Item(
            name = item_details['name'],
            category = item_details['category'],
            type = item_details['type'],
            company = item_details['company'],
            unit = item_details['unit'],
            volume = item_details['volume'],
        )
        #add and commit the new item to the session
        db.session.add(item)
        db.session.commit()

        return ItemSchema().dump(item), 201 #Return Created Item
    except:
        ValueError
        return ({'error': 'item with that name already exists'}), 409 #Resource already exists 

#Find an item:
@items_bp.route('/<int:item_id>')
def one_item(item_id):
  stmt = db.select(Item).filter_by(id=item_id)
  item = db.session.scalar(stmt)
  if item:
    return ItemSchema().dump(item)
  else:
    return {'error': 'Item not found'}, 404

#Delete an item:
@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    stmt = db.select(Item).filter_by(id=item_id)
    item = db.session.scalar(stmt)
    if item:
        db.session.delete(item)
        db.session.commit()
        return ('Item Deleted'), 200
    else:
        return{'error': 'Item does not exist'}, 404
    

#Update an item
@items_bp.route('/<int:item_id>', methods=['PUT', 'PATCH'])
def update_item(item_id):
  stmt = db.select(Item).filter_by(id=item_id)
  item = db.session.scalar(stmt)
  item_info = ItemSchema().load(request.json)
  if item:
    item.name = item_info.get('name', item.name)
    item.category = item_info.get('category', item.category)
    item.type = item_info.get('type', item.type)
    item.company = item_info.get('company', item.company)
    item.unit = item_info.get('unit', item.unit)
    item.volume = item_info.get('volume', item.volume)
    db.session.commit()
    return ItemSchema().dump(item)
  else:
    return {'error': 'item not found'}, 404
  
 
#Add all items from the Item Table to the Stock Table, with available-quantities set to 10
@items_bp.route('/stock_all', methods=['POST'])
def add_all_to_stock():
    items = Item.query.all()
    
    for item in items:
        stock = Stock(
            item_id = item.id,
            name = item.name,
            category = item.category,
            type = item.type,
            available_stock = 10,
            cost_price = 0
        )
        
        db.session.add(stock)
    
    db.session.commit()
    if item:
        return ({'message': 'All items added to stock'}), 201
    else:
       return {'error': 'item not found'}, 404

#Clear Table
@items_bp.route('/clear', methods=['DELETE'])
def clear_table():
   Item.query.delete()
   db.session.commit()
   return ('Table Cleared'), 200 


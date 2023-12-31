from flask import Blueprint, request
from init import db
from models.bar import Bar, BarSchema
from models.stock import Stock



bar_bp = Blueprint('bar', __name__, url_prefix='/bar')

@bar_bp.route('/')
def bar():
    stmt = db.Select(Bar).order_by(Bar.quantity.desc())
    bar = db.session.scalars(stmt).all()
    if bar:
        return BarSchema(many=True).dumps(bar)
    else:
        return {'error': 'No bar items found'}, 404

#Add item from stock table to the bar table
@bar_bp.route('/<int:id>', methods=['POST'])
def add_to_bar(id):
    try:
        bar_item_details = BarSchema().load(request.json)
        stmt = db.select(Stock).filter_by(stock_id=id)
        stock_item = db.session.scalar(stmt)

        #Check if an item with the same name already exists
        existing_item = Bar.query.filter_by(stock_id=stock_item.stock_id).first()
        if existing_item:
            raise ValueError
        
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
            return ({'error': 'Item not found'}), 404
    except:
        ValueError
        return ({'error': 'bar item with that name already exists'}), 409 #Resource already exists 

#Example:
#Remember to add the item Id to the URL first, e.g.: localhost:5000/bar/4
#JSON input:
#{ 
#     "quantity": 8,
#     "target_quantity": 10
#}


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
@bar_bp.route('/<int:bar_id>', methods=['DELETE'])
def delete_item(bar_id):
    stmt = db.select(Bar).filter_by(bar_id=bar_id)
    bar_item = db.session.scalar(stmt)
    if bar_item:
        db.session.delete(bar_item)
        db.session.commit()
        return ('Bar Item Deleted'), 200
    else:
        return{'error': 'Bar Item does not exist'}, 404


#Update an item
@bar_bp.route('/<int:bar_id>', methods=['PATCH'])
def update_item(bar_id):
  stmt = db.select(Bar).filter_by(bar_id=bar_id)
  bar_item = db.session.scalar(stmt)
  bar_item_info = BarSchema().load(request.json)
  if bar_item:
    bar_item.quantity = bar_item_info.get('quantity', bar_item.quantity) #input quantity through JSON load
    bar_item.target_quantity = bar_item_info.get('target_quantity', bar_item.target_quantity) #input target_quantity through JSON load
    
    db.session.commit()
    return BarSchema().dump(bar_item)
  else:
    return {'error': 'bar item not found'}, 404
  
#Clear Bar Table
@bar_bp.route('/clear', methods=['DELETE'])
def clear_table():
    Bar.query.delete()
    db.session.commit()
    return{}, 200


#Add all items from the Stock Table to the Bar Table
@bar_bp.route('/add_all', methods=['POST'])
def add_all():
    stock = Stock.query.all()
    for stock_item in stock:
        bar = Bar(
            stock_id = stock_item.stock_id,
            name = stock_item.name,
            category = stock_item.category,
            type = stock_item.type,
            quantity = 8,
            target_quantity = 10,
            bar_price = 15
        )
        
        db.session.add(bar)
        db.session.commit()
    if stock_item:
        return ('All items added to bar inventory'), 201
    else:
       return {'error': 'stock item not found'}, 404

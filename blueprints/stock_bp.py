from flask import Blueprint, request, jsonify
from init import db
from models.stock import Stock, StockSchema
from models.items import Item, ItemSchema
from psycopg2 import IntegrityError




stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

# @stock_bp.route('/')
# def index():
#     return 'Hello, world'

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


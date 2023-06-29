from flask import Blueprint, request
from models.items import *
from models.stock import *
from models.bar import *
from models.stock_list import *

items_bp = Blueprint('items', __name__, url_prefix='/items')


@items_bp.route('/')
def items():
    stmt = db.Select(Item).order_by(Item.category.desc())
    item = db.session.scalars(stmt).all()
    return ItemSchema(many=True).dumps(item)


@items_bp.route('/add', methods=['POST'])
def add_stock():
    #Load POST data via the Schema
    item_details = ItemSchema().load(request.json)
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

    return ItemSchema().dump(item), 201
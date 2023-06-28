from flask import Blueprint
from init import db
from models.items import Item, ItemSchema
from models.stock import Stock, StockSchema
from models.bar import Bar, BarSchema
from models.stock_list import Stock_list, Stock_list_Schema




auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return 'Hello, world'


@auth_bp.route('/items')
def items():
    stmt = db.Select(Item).order_by(Item.category.desc())
    item = db.session.scalars(stmt).all()
    return ItemSchema(many=True).dumps(item)

@auth_bp.route('/stock')
def stock():
    stmt = db.Select(Stock).order_by(Stock.quantity.desc())
    stock = db.session.scalars(stmt).all()
    return StockSchema(many=True).dumps(stock)

@auth_bp.route('/bar')
def bar():
    stmt = db.Select(Bar).order_by(Bar.quantity.desc())
    bar = db.session.scalars(stmt).all()
    return BarSchema(many=True).dumps(bar)

@auth_bp.route('/stock_list')
def stocklist():
    stmt = db.Select(Stock_list).order_by(Stock_list.category.asc())
    stock_list = db.session.scalars(stmt).all()
    return Stock_list_Schema(many=True).dumps(stock_list)
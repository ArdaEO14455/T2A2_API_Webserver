from flask import Blueprint
from init import db
from models.stock_list import Stock_list, Stock_list_Schema




stocklist_bp = Blueprint('stocklist', __name__, url_prefix='/stock_list')

@stocklist_bp.route('/')
def stocklist():
    stmt = db.Select(Stock_list).order_by(Stock_list.category.asc())
    stock_list = db.session.scalars(stmt).all()
    return Stock_list_Schema(many=True).dumps(stock_list)
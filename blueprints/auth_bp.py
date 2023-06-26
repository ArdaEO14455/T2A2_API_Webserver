from flask import Blueprint
from models.inventory import *




auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return 'Hello, world'


@auth_bp.route('/stock')
def stock():
    stmt = db.Select(Stock).order_by(Stock.quantity.desc())
    stock = db.session.scalars(stmt).all()
    return StockSchema(many=True).dumps(stock)
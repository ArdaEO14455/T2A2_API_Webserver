from flask import Blueprint
from init import db
from models.bar import Bar, BarSchema



bar_bp = Blueprint('bar', __name__, url_prefix='/bar')

@bar_bp.route('/')
def bar():
    stmt = db.Select(Bar).order_by(Bar.quantity.desc())
    bar = db.session.scalars(stmt).all()
    return BarSchema(many=True).dumps(bar)


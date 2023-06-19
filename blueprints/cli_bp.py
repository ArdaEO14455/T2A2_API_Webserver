from flask import Blueprint
from init import db


cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Stock Tables Created Successfully')

@cli_bp.cli.command('stock_list')
def seed_db():
    pass
from flask import Blueprint
from init import db
from models.inventory import *
from models.items import *

stock_bp = Blueprint('stock', __name__)
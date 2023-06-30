from flask import Blueprint, jsonify


index_bp = Blueprint('/', __name__, url_prefix='')

@index_bp.route('/')
def index():
    return jsonify(
        {'Welcome': "Hello, and welcome to Stock Management! if you'd like to view the different databases, follow the handy directions below"},
        {'Items Table':"if you'd like to view with the items table, initiate a GET request after appending your current url with 'items/' or after clicking /items "},
        {'Stock Table':"if you'd like to view with the stock table, initiate a GET request after appending your current url with 'stock/' or after clicking /stock "},
        {'Bar Table':"if you'd like to view with the bar table, initiate a GET request after appending your current url with 'bar/' or after clicking /bar "},
        {'Stocklist Table':"if you'd like to view with the stocklist table, initiate a GET request after appending your current url with 'stocklist/' or after clicking /stocklist "},
        {'Items Table':"for additional information to view with the data within each table, please see the README.md document in the root directory"}
    )

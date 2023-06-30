from flask import Flask
from os import environ
from init import db, ma
from blueprints.index_bp import index_bp
from blueprints.cli_bp import cli_bp
from blueprints.stock_bp import stock_bp
from blueprints.items_bp import items_bp
from blueprints.stock_list_bp import stocklist_bp
from blueprints.bar_bp import bar_bp
from init import db, ma



def setup():
    app = Flask(__name__)
#Database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

#Initialize Database and Marshmallow
    db.init_app(app)
    ma.init_app(app)

#Blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(cli_bp)
    app.register_blueprint(items_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(bar_bp)
    app.register_blueprint(stocklist_bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app
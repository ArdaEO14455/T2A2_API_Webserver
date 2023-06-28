from flask import Flask
from os import environ
from init import db, ma
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from init import db, ma


def setup():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    # app.register_blueprint(stock_bp)

    if __name__ == '__main__':
        app.run(debug=True)
        
    return app
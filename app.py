from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://stock_taker:password@localhost:5432/stock'

db = SQLAlchemy(app)

class Stock_List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    company = db.Column(db.Text())
    quantity = db.Column(db.Integer)

@app.cli.command('create')
def create_db():
    db.create_all()
    print('Stock Tables Created Successfully')

@app.route('/')
def index():
    return 'Hello, world'

if __name__ == '__main__':
    app.run(debug=True)
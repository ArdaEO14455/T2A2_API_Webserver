from flask import Blueprint




auth_bp = Blueprint('auth', __name__)

@app.route('/')
def index():
    return 'Hello, world'
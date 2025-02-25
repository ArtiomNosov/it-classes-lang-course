from flask import Flask
from app.api.routes import bp as route_bp
from app.api.get_code_from_request import get_code
from app.api.get_code_from_request import bp as get_code_bp
from app.api.user_authorization import bp as profile_bp
from app.api.ask_question import bp as ask_bp
from app.db import create_db
from app.db.actions import view_database, save_user_to_db
import secrets


app = Flask(__name__, static_folder="app/frontend/static", template_folder="app/frontend/templates")
app.register_blueprint(get_code_bp)
app.register_blueprint(route_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(ask_bp)
app.config['SECRET_KEY'] = '66d3649233faf31ef4f56348aad2cff4'

if __name__ == '__main__':
    create_db.create_db()
    view_database()
    app.run(debug=any)
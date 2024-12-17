from flask import Flask
from app.api.routes import bp as route_bp
from app.api.get_code_from_request import get_code
from app.api.get_code_from_request import bp as get_code_bp
from app.db import create_db

app = Flask(__name__, static_folder="app/frontend/static", template_folder="app/frontend/templates")
app.register_blueprint(get_code_bp)
app.register_blueprint(route_bp)

if __name__ == '__main__':
    create_db.create_db()
    app.run(debug=any)
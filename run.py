from flask import Flask
from app.routes import bp as route_bp
from app.get_code_from_request import get_code
from app.get_code_from_request import bp as get_code_bp
app = Flask(__name__)
app.register_blueprint(get_code_bp)
app.register_blueprint(route_bp)
# get_code()

if __name__ == '__main__':
    app.run(debug=any)
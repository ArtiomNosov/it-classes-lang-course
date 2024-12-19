from flask import Blueprint, render_template, request, send_from_directory, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/forum')
def forum_page():
    return render_template('forum_page.html')

@bp.route('/login')
def login_page():
    return render_template('login.html')

@bp.route('/register')
def register_page():
    return render_template('register.html')


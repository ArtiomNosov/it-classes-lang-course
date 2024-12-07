from flask import Blueprint, render_template, request, send_from_directory, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/')
def serve_html():
    return send_from_directory('app', 'index.html')


from flask import Blueprint, render_template, request, send_from_directory, jsonify

bp = Blueprint('get_code', __name__)

@bp.route('/submit', methods=['POST'])
def get_code():
    data = request.json
    print(f"Received data: {data}")  # Логируем входящие данные
    
    code = data.get('code')

    file_path = "app/user_code"

    with open (file_path, 'w') as file:
        file.write(code)
        print(f"Code saved successfully to {file_path}")
    
    return jsonify({"message": "Code saved successfully", "file_path": file_path}), 200

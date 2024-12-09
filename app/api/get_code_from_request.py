from flask import Blueprint, render_template, request, send_from_directory, jsonify
from app.api.docker_compiling_cpp.compile_cpp import save_cpp

bp = Blueprint('get_code', __name__)

@bp.route('/submit', methods=['POST'])
def get_code():
    # Получаем код из запроса
    data = request.json
    print(f"Received data: {data}")  # Логируем входящие данные
    
    code = data.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Сохраняем код в файл
    file_path = "app/api/docker_compiling_cpp/main.cpp"
    with open(file_path, 'w') as file:
        file.write(code)
        print(f"Code saved successfully to {file_path}")

    # Теперь компилируем код
    result = save_cpp()

    # Возвращаем результат компиляции
    return jsonify({
        "message": "Code saved and compiled successfully",
        "file_path": file_path,
        "compiled_output": result
    }), 200
from flask import Blueprint, request, jsonify, url_for, current_app
from app.api.docker_compiling_cpp.compile_cpp import save_cpp
import requests

bp = Blueprint('get_code', __name__)

@bp.route('/submit', methods=['POST'])
def get_code():
    try:
        # Получаем код из запроса
        data = request.json
        code = data.get('code')
        if not code:
            return jsonify({"error": "No code provided"}), 400

        # Сохраняем код в файл
        file_path = "app/api/docker_compiling_cpp/main.cpp"
        with open(file_path, 'w') as file:
            file.write(code)

        # Компилируем код
        result = save_cpp()

        # Возвращаем результат компиляции
        return jsonify({
            "message": "Code compiled successfully",
            "compiled_output": result
        }), 200
    except Exception as e:
        # Возвращаем JSON-ответ при ошибке
        return jsonify({"error": str(e)}), 500



def send_to_submit(code):
    """
    Функция для отправки POST-запроса на альтернативный маршрут.
    """
    # Получаем URL альтернативного маршрута через Flask
    with current_app.test_request_context():
        url = url_for('get_code.trigger_submit', _external=True)  # Используем другой маршрут
    
    # Отправляем POST-запрос
    try:
        response = requests.post(url, json={"code": code})
        if response.ok:
            print("Response received successfully!")
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return {"error": response.text}
    except Exception as e:
        print(f"Exception during request: {e}")
        return {"error": str(e)}


@bp.route('/trigger', methods=['POST'])
def trigger_submit():
    """
    Альтернативный маршрут для обработки внутренних вызовов.
    """
    data = request.json
    code = data.get('code', '')
    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Пример внутренней обработки (компиляция или иные действия)
    return jsonify({"message": "Triggered successfully", "code": code})

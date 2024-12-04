'''
здесь по пути /submit мы принимаем запрос с кодом, обрабатываем его и запихиваем в файлик (пока что, потом возможно будет как то по другому)
'''


from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Путь для сохранения файлов
UPLOAD_DIR = "./user_code"
# Убедимся, что директория существует
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def serve_html():
    return send_from_directory('static', 'index.html')

@app.route('/submit', methods=['POST'])
def submit_code():
    data = request.get_json()
    print(f"Received data: {data}")  # Логируем входящие данные

    code = data.get('code')

    # Печатаем путь к файлу для отладки
    file_path = os.path.join(UPLOAD_DIR, "user_code.cpp")
    # print(f"Saving code to: {file_path}")

    try:
        # Сохраняем код в файл
        with open(file_path, 'w') as code_file:
            code_file.write(code)
        print(f"Code saved successfully to {file_path}")
    except Exception as e:
        print(f"Error saving code: {e}")
        return jsonify({"error": f"Error saving code: {str(e)}"}), 500

    return jsonify({"message": "Code saved successfully", "file_path": file_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

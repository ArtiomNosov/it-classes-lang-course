from flask import request, jsonify, Blueprint, render_template,session
from app.db.actions import save_question_to_db
bp = Blueprint("question", __name__)

@bp.route('/submit_question', methods=['POST'])
def submit_question():
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in session:
        return jsonify({'message': 'Пользователь не авторизован'}), 401

    # Извлекаем данные из запроса
    data = request.json
    title = data.get('title')
    text = data.get('text')
    user_id = session['user_id']  # Получаем ID пользователя из сессии

    # Проверяем обязательные поля
    if not title or not text:
        return jsonify({'message': 'Заголовок и текст вопроса обязательны'}), 400

    # Сохраняем вопрос в базу данных
    save_question_to_db(title, text, user_id)

    return jsonify({'message': 'Вопрос успешно отправлен', 'title': title}), 200
@bp.route("/new_question")
def new_question():
    return render_template("ask_question.html")
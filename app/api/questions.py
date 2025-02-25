from flask import request, jsonify, Blueprint, render_template,session
from app.db.actions import save_question_to_db, get_user_questions, get_question_by_id,update_votes
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


@bp.route("/my_questions")
def my_questions():
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in session:
        return "Вы не авторизованы", 401

    # Получаем ID пользователя из сессии
    user_id = session['user_id']

    # Запрашиваем вопросы из базы данных
    questions = get_user_questions(user_id)

    # Передаем данные в шаблон
    return render_template("my_questions.html", questions=questions)


from flask import render_template, abort

@bp.route("/question/<int:question_id>")
def view_question(question_id):
    # Получаем данные вопроса из базы данных
    question = get_question_by_id(question_id)

    if not question:
        abort(404)  # Возвращаем ошибку 404, если вопрос не найден

    # Передаем данные в шаблон
    return render_template("view_question.html", question=question)

from flask import jsonify

@bp.route("/vote/<int:question_id>", methods=["POST"])
def vote_question(question_id):
    # Проверяем, авторизован ли пользователь
    if 'user_id' not in session:
        return jsonify({'message': 'Пользователь не авторизован'}), 401

    # Получаем ID пользователя из сессии
    user_id = session['user_id']

    # Получаем действие из тела запроса
    data = request.get_json()
    action = data.get('action')  # Должно быть 'upvote' или 'downvote'

    if action not in ['upvote', 'downvote']:
        return jsonify({'message': 'Неверное действие'}), 400

    # Обновляем счетчик лайков в базе данных
    success = update_votes(question_id, user_id, action)  # Передаем user_id
    if success:
        # Получаем обновленные данные вопроса
        question = get_question_by_id(question_id)
        return jsonify({'likes': question['likes']}), 200
    else:
        return jsonify({'message': 'Ошибка при голосовании'}), 500
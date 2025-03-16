from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify
from app.db.actions import save_user_to_db, authenticate_user, get_user_by_username, get_user_by_id

bp = Blueprint('profile', __name__)

# Маршрут для входа в систему
from flask import jsonify, session

@bp.route("/submit_login", methods=["POST"])
def submit_login():
    # Получаем данные из запроса
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Проверяем учетные данные
    user = authenticate_user(username, password)  # Функция для проверки данных
    if user:
        # Сохраняем ID пользователя в сессии
        session['user_id'] = user['id']

        # Возвращаем JSON с ID пользователя
        return jsonify({'user_id': user['id']}), 200
    else:
        return jsonify({'message': 'Неверный логин или пароль'}), 401

from flask import abort
# Маршрут для просмотра профиля
# @bp.route("/profile/<int:user_id>")
# def view_profile(user_id):
#     # Получаем данные пользователя из базы данных
#     user = get_user_by_id(user_id)

#     if not user:
#         abort(404)  # Возвращаем ошибку 404, если пользователь не найден

#     # Передаем данные в шаблон
#     return render_template("profile.html", user=user)


# Маршрут для выхода из системы
@bp.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    print("Пользователь вышел из системы")  # Логирование выхода
    # Редирект на главную страницу или страницу входа
    return redirect("/")  # Предполагается, что у вас есть маршрут auth.login

@bp.route("/profile/<int:user_id>")
def view_profile(user_id):
    # Получаем данные пользователя из базы данных
    user = get_user_by_id(user_id)

    if not user:
        abort(404)  # Возвращаем ошибку 404, если пользователь не найден

    # Передаем данные в шаблон
    return render_template("profile.html", user=user)

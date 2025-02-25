from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify
from app.db.actions import save_user_to_db, authenticate_user, get_user_by_username

bp = Blueprint('profile', __name__)

# Маршрут для входа в систему
@bp.route('/submit_login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Логин и пароль обязательны'}), 400

    if authenticate_user(username, password):  # Проверка аутентификации
        session['username'] = username  # Сохранение имени пользователя в сессии
        print(f"Session Username: {session.get('username')}")  # Логирование данных сессии
        return jsonify({'message': 'Все ок'}), 200
    else:
        return jsonify({'message': 'Неверный логин или пароль'}), 401

# Маршрут для просмотра профиля
@bp.route('/profile')
def profile():
    username = session.get('username')
    print(f"Session Username: {username}")  # Логирование данных сессии

    if not username:
        return 'Вы не авторизованы', 401

    user_data = get_user_by_username(username)
    if not user_data:
        return 'Пользователь не найден', 404

    return render_template('profile.html', user=user_data)

# Маршрут для выхода из системы
@bp.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.pop('username', None)
    print("Пользователь вышел из системы")  # Логирование выхода
    # Редирект на главную страницу или страницу входа
    return redirect(url_for('routes.index'))  # Предполагается, что у вас есть маршрут auth.login
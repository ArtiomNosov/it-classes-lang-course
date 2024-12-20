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

@bp.route('/submit_login', methods=['POST'])
def login():
    
    # Получаем данные из запроса
    data = request.json
    username = data.get('username')
    password = data.get('password')
    remember_me = data.get('remember_me')
    print(username,password,remember_me)
    # Проверяем полученные данные
    
    if not username or not password:
        return jsonify({'message': 'Логин и пароль обязательны'}), 400

    '''
    ване написать функцию которая сверяет логин и пароль 
    (пароль надо расхэшировать, уже писал фунцкцию в passwords.py) из бд
    '''

    # Например, проверяем пользователя в базе данных
    if username == 'admin' and password == '1234':  # Здесь пример проверки
        return jsonify({'message': 'Успешный вход', 'username': username}), 200
    else:
        return jsonify({'message': 'Неверный логин или пароль'}), 401

@bp.route('/new_register', methods = ['POST'])
def register():

    # Получаем данные из запроса
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    print(f'Получены данные: username={username}, email={email}, password={password}')
    
    # Проверяем обязательные поля
    if not username or not email or not password:
        return jsonify({'message': 'Все поля обязательны для заполнения'}), 400
    
    # Проверяем уникальность пользователя (пример)
    # Здесь предполагается, что в базе данных есть проверка на уникальность
    if username == 'existing_user':  # Пример проверки
        return jsonify({'message': 'Логин уже занят'}), 409

    # Регистрация прошла успешно
    return jsonify({'message': 'Успешная регистрация', 'username': username}), 201

@bp.route('/register')
def register_page():
    return render_template('register.html')


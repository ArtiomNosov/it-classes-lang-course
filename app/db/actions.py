import sqlite3
from app.db import passwords


def save_user_to_db(username, email, password):
    try:
        conn = sqlite3.connect('app/db/users.db')
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь с данным email или username
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            print(f"Пользователь с email '{email}' уже существует.")
            return

        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            print(f"Пользователь с логином '{username}' уже существует.")
            return

        # Хэшируем пароль
        hashed_password = passwords.hash_password(password)
        print(f"Хэшированный пароль: {hashed_password}")

        # Вставляем данные в таблицу
        cursor.execute('''
            INSERT INTO users (username, email, password) VALUES (?, ?, ?)
        ''', (username, email, hashed_password))

        conn.commit()
        print(f"Пользователь '{username}' успешно добавлен в базу данных.")
    except sqlite3.IntegrityError as e:
        print(f"Ошибка уникальности: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        conn.close()


def authenticate_user(username, password_to_check):
    conn = sqlite3.connect('app/db/users.db')
    cursor = conn.cursor()

    # Получаем хэш пароля пользователя по логину (username)
    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    
    stored_hash = cursor.fetchone()

    conn.close()

    if stored_hash:
        # Проверяем пароль
        if passwords.check_password(stored_hash[0], password_to_check):
            print(f"Пользователь '{username}' успешно аутентифицирован.")
            return True
        else:
            print("Неверный пароль.")
            return False
    else:
        print("Пользователь не найден.")
        return False

import os
def view_database():
    # Подключаемся к базе данных
    # db_path = os.path.abspath()
    conn = sqlite3.connect('app/db/users.db')
    cursor = conn.cursor()
    
    # Проверяем список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Таблицы в базе данных:", tables)

    # Выводим содержимое таблицы 'users' (если существует)
    try:
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        print("Содержимое таблицы 'users':")
        for user in users:
            print(user)
    except sqlite3.OperationalError as e:
        print("Ошибка:", e)

    # Закрываем соединение
    conn.close()

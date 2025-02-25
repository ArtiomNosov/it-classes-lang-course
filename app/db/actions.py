import sqlite3
from app.db import passwords


def save_user_to_db(username, email, password):
    try:
        conn = sqlite3.connect('app/db/forum.db')
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
    conn = sqlite3.connect('app/db/forum.db')
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
    conn = sqlite3.connect('app/db/forum.db')
    cursor = conn.cursor()
    
    # Проверяем список таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Таблицы в базе данных:", tables)

    # Выводим содержимое таблицы 'users' (если существует)
    try:
        cursor.execute("SELECT * FROM questions;")
        users = cursor.fetchall()
        print("Содержимое таблицы 'questions':")
        for user in users:
            print(user)
    except sqlite3.OperationalError as e:
        print("Ошибка:", e)

    # Закрываем соединение
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('app/db/forum.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {'id': user[0], 'username': user[1], 'email': user[2]}
    return None

def save_question_to_db(title, body, author_id):
    """
    Сохраняет новый вопрос в базу данных.

    :param title: Заголовок вопроса (str)
    :param body: Текст вопроса (str)
    :param author_id: ID автора вопроса (int)
    """
    # Подключение к базе данных
    conn = sqlite3.connect('app/db/forum.db')  # Замените 'your_database.db' на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        # Вставка данных в таблицу questions
        cursor.execute('''
            INSERT INTO questions (title, body, author_id, likes)
            VALUES (?, ?, ?, ?)
        ''', (title, body, author_id, 0))  # likes устанавливаем в 0 по умолчанию

        # Фиксация изменений
        conn.commit()
    except sqlite3.Error as e:
        # В случае ошибки выводим сообщение
        print(f"Ошибка при сохранении вопроса: {e}")
        conn.rollback()  # Откатываем изменения в случае ошибки
    finally:
        # Закрываем соединение с базой данных
        conn.close()

def get_user_questions(user_id):
    """
    Получает все вопросы, заданные пользователем, из базы данных.

    :param user_id: ID пользователя (int)
    :return: Список словарей с данными вопросов
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, title, body, likes, created_at
            FROM questions
            WHERE author_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        rows = cursor.fetchall()

        # Преобразуем результат в список словарей
        questions = []
        for row in rows:
            questions.append({
                'id': row[0],
                'title': row[1],
                'body': row[2],
                'likes': row[3],
                'created_at': row[4]
            })
        return questions
    except sqlite3.Error as e:
        print(f"Ошибка при получении вопросов: {e}")
        return []
    finally:
        conn.close()
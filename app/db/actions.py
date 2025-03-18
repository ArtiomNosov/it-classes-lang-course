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

    try:
        # Получаем хэш пароля и ID пользователя по логину
        cursor.execute('''
            SELECT id, username, password FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()

        if user_data:
            user_id, username, stored_hash = user_data

            # Проверяем пароль
            if passwords.check_password(stored_hash, password_to_check):
                print(f"Пользователь '{username}' успешно аутентифицирован.")
                return {'id': user_id, 'username': username}  # Возвращаем данные пользователя
            else:
                print("Неверный пароль.")
                return None
        else:
            print("Пользователь не найден.")
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при аутентификации: {e}")
        return None
    finally:
        conn.close()
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

def get_question_by_id(question_id):
    """
    Получает данные вопроса из базы данных по его ID.

    :param question_id: ID вопроса (int)
    :return: Словарь с данными вопроса или None, если вопрос не найден
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT id, title, body, author_id, likes, created_at
            FROM questions
            WHERE id = ?
        ''', (question_id,))
        row = cursor.fetchone()

        if row:
            return {
                'id': row[0],
                'title': row[1],
                'body': row[2],
                'author_id': row[3],
                'likes': row[4],
                'created_at': row[5]
            }
        return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении вопроса: {e}")
        return None
    finally:
        conn.close()

def update_votes(question_id, user_id, action):
    """
    Обновляет счетчик лайков для вопроса.
    :param question_id: ID вопроса (int)
    :param user_id: ID пользователя (int)
    :param action: Действие ('upvote' или 'downvote')
    :return: True, если обновление успешно, иначе False
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        # Проверяем, голосовал ли пользователь ранее
        cursor.execute('''
            SELECT vote_type FROM votes
            WHERE question_id = ? AND user_id = ?
        ''', (question_id, user_id))
        existing_vote = cursor.fetchone()

        likes_change = 0  # Изменение счетчика лайков

        if existing_vote:
            old_vote_type = existing_vote[0]
            if old_vote_type == action:
                # Если пользователь повторно нажимает ту же кнопку, отменяем его голос
                cursor.execute('''
                    DELETE FROM votes
                    WHERE question_id = ? AND user_id = ?
                ''', (question_id, user_id))
                likes_change = -1 if old_vote_type == 'upvote' else 1
            else:
                # Если пользователь меняет свой голос
                cursor.execute('''
                    UPDATE votes
                    SET vote_type = ?
                    WHERE question_id = ? AND user_id = ?
                ''', (action, question_id, user_id))
                likes_change = 2 if action == 'upvote' else -2
        else:
            # Если пользователь голосует впервые
            cursor.execute('''
                INSERT INTO votes (question_id, user_id, vote_type)
                VALUES (?, ?, ?)
            ''', (question_id, user_id, action))
            likes_change = 1 if action == 'upvote' else -1

        # Обновляем счетчик лайков в таблице questions
        cursor.execute('''
            UPDATE questions
            SET likes = likes + ?
            WHERE id = ?
        ''', (likes_change, question_id))

        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении лайков: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_all_questions():
    """
    Получает все вопросы из базы данных с никнеймами авторов.

    :return: Список словарей с данными вопросов
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT q.id, q.title, q.likes, q.created_at, u.username
            FROM questions q
            LEFT JOIN users u ON q.author_id = u.id
            ORDER BY q.created_at DESC
        ''')
        rows = cursor.fetchall()

        # Преобразуем результат в список словарей
        questions = []
        for row in rows:
            questions.append({
                'id': row[0],
                'title': row[1],
                'likes': row[2],
                'created_at': row[3],
                'author_username': row[4]  # Никнейм автора
            })
        return questions
    except sqlite3.Error as e:
        print(f"Ошибка при получении вопросов: {e}")
        return []
    finally:
        conn.close()

import sqlite3

def get_user_by_id(user_id):
    """
    Получает данные пользователя из базы данных по его ID.

    :param user_id: ID пользователя (int)
    :return: Словарь с данными пользователя или None, если пользователь не найден
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT 
                id, 
                username, 
                email, 
                registration_date, 
                questions_count, 
                answers_count, 
                likes 
            FROM users
            WHERE id = ?
        ''', (user_id,))
        row = cursor.fetchone()

        if row:
            # Формируем словарь с данными пользователя
            return {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'registration_date': row[3],
                'questions_count': row[4],
                'answers_count': row[5],
                'likes': row[6]
            }
        return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        conn.close()

import sqlite3
from datetime import datetime

def add_answer(question_id, user_id, body):
    """
    Добавляет ответ в базу данных.

    :param question_id: ID вопроса (int)
    :param user_id: ID пользователя (int)
    :param body: Текст ответа (str)
    :return: True, если добавление успешно, иначе False
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO answers (question_id, author_id, body, created_at)
            VALUES (?, ?, ?, ?)
        ''', (question_id, user_id, body, datetime.now()))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении ответа: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_answers_for_question(question_id):
    """
    Получает все ответы для конкретного вопроса.

    :param question_id: ID вопроса (int)
    :return: Список словарей с данными ответов
    """
    conn = sqlite3.connect('app/db/forum.db')  # Замените на путь к вашей базе данных
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT a.id, a.body, a.created_at, u.username
            FROM answers a
            LEFT JOIN users u ON a.author_id = u.id
            WHERE a.question_id = ?
            ORDER BY a.created_at ASC
        ''', (question_id,))
        rows = cursor.fetchall()

        answers = []
        for row in rows:
            answers.append({
                'id': row[0],
                'body': row[1],
                'created_at': row[2],
                'author_username': row[3]
            })
        return answers
    except sqlite3.Error as e:
        print(f"Ошибка при получении ответов: {e}")
        return []
    finally:
        conn.close()
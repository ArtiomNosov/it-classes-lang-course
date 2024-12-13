import sqlite3
from app.db import passwords

def save_user_to_db(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Хэшируем пароль
    hashed_password = passwords.hash_password(password)

    # Вставляем данные в таблицу
    cursor.execute('''
        INSERT INTO users (email, password) VALUES (?, ?)
    ''', (email, hashed_password))

    conn.commit()
    conn.close()

def authenticate_user(email, password_to_check):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Получаем хэш пароля пользователя по email
    cursor.execute('''
        SELECT password FROM users WHERE email = ?
    ''', (email,))
    
    stored_hash = cursor.fetchone()

    conn.close()

    if stored_hash:
        # Проверяем пароль
        if passwords.check_password(stored_hash[0], password_to_check):
            print("User authenticated successfully")
        else:
            print("Invalid password")
    else:
        print("User not found")

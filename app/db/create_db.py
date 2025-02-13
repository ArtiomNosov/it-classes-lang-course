import sqlite3
import os

def create_db():
    # Подключаемся к базе данных
    conn = sqlite3.connect("app/db/forum.db")
    cursor = conn.cursor()

    # Создаём таблицу users, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            levels_completed INTEGER DEFAULT 0
        )
    ''')

    # Создаём таблицу questions, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            author_id INTEGER,
            likes INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

    print(f"База данных создана или уже существует: app/db/forum.db")

if __name__ == '__main__':
    create_db()

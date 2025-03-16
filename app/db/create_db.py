import sqlite3
import os

def create_db():
    # Путь к базе данных
    db_path = "app/db/forum.db"
    
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаём таблицу users, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            levels_completed INTEGER DEFAULT 0,
            questions_count INTEGER DEFAULT 0,   -- Количество заданных вопросов
            answers_count INTEGER DEFAULT 0,     -- Количество ответов
            registration_date TEXT DEFAULT (CURRENT_TIMESTAMP)  -- Дата регистрации
        )
    ''')

    # Создаём таблицу questions, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            author_id INTEGER,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users(id)
        )
    ''')

    # Создаём таблицу votes, если она ещё не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            vote_type TEXT NOT NULL, -- 'upvote' или 'downvote'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(question_id, user_id) -- Один пользователь может проголосовать только один раз за вопрос
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                author_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions(id),
                FOREIGN KEY (author_id) REFERENCES users(id)
            )
        ''')
    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print(f"База данных создана или уже существует: {db_path}")

if __name__ == '__main__':
    # Создаем директорию для базы данных, если она не существует
    os.makedirs("app/db", exist_ok=True)
    create_db()
import sqlite3
import os

def create_db():
    path = os.getcwd()
    path = os.path.join("app/db/users.db")
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            levels_completed INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

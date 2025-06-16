import sqlite3
def init_db():
    conn = sqlite3.connect('stocks_bot.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        join_date TEXT
    )
    ''')

    # Таблица компаний
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        ticker TEXT PRIMARY KEY,
        name TEXT
    )
    ''')

    # Таблица подписок (связь пользователей и компаний)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscriptions (
    user_id INTEGER,
    ticker TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (ticker) REFERENCES companies (ticker),
    PRIMARY KEY (user_id, ticker)
)
''')

    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()
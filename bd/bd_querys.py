import sqlite3
from datetime import datetime
async def get_list_of_subscriptions(chat_id):
    try:
        conn = sqlite3.connect("bd/stocks_bot.db")
        cursor = conn.cursor()

        cursor.execute('''
        SELECT c.ticker, c.name 
        FROM subscriptions s
        JOIN companies c ON s.ticker = c.ticker
        WHERE s.user_id = ?
        ''', (chat_id,))
        user_subscriptions = cursor.fetchall()
        conn.close()
        print(f"Получен список подписок {chat_id}")
        return user_subscriptions

    except sqlite3.Error as e:
        print(f"Ошибка при получении подписок: {e}")
        return []
    # return [("LIFE", "life"), ("LKOH", "Лукоил")]
async def is_subscribed_to(chat_id, ticker): #REMAKE THIS
    lst = await get_list_of_subscriptions(chat_id)
    for i, _ in lst:
        if i == ticker:
            return True
    return False

async def subscribe(chat_id, ticker):
    try:
        conn = sqlite3.connect("bd/stocks_bot.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO subscriptions (user_id, ticker)
            VALUES (?, ?)
            ''', (chat_id, ticker))
        conn.commit()
        print(f"new subscribe {chat_id}, {ticker}")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при подписке: {e}")
        return False

async def unsubcribe(chat_id, ticker):
    try:
        conn = sqlite3.connect("bd/stocks_bot.db")
        cursor = conn.cursor()
        cursor.execute('''
               DELETE FROM subscriptions 
               WHERE user_id = ? AND ticker = ?
               ''', (chat_id, ticker))
        conn.commit()
        print(f"unsubscribed {chat_id}, {ticker}")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при отписке: {e}")
        return False
async def register_user(chat_id, name=""):
    try:
        date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect("bd/stocks_bot.db")
        cursor = conn.cursor()
        datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, join_date)
            VALUES (?, ?, ?)
            ''', (chat_id, name, date,))
        conn.commit()
        print(f"new user {chat_id}")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при регистрации : {e}")
        return False
async def register_company(ticker):
    print("empty function")
    pass
async def is_compony_registred(ticker):
    try:
        conn = sqlite3.connect("bd/stocks_bot.db")
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM companies WHERE ticker = ?", (ticker,))
        exists = cursor.fetchone() is not None

        conn.close()
        print(f"Успешная проверка существования компании {ticker}")
        return exists

    except sqlite3.Error as e:
        print(f"Ошибка при проверке тикера: {e}")
        return False
import sqlite3
import requests
def main():
    companies = fetch_moex_companies()
    if companies:
        save_to_database(companies)
    else:
        print("Не удалось получить данные с MOEX")

def fetch_moex_companies():
    """Получает список компаний с MOEX API"""
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json"
    params = {
        'iss.meta': 'off',
        'securities.columns': 'SECID,SECNAME'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        securities = data['securities']['data']
        return [(sec[0], sec[1]) for sec in securities]  # (ticker, name)
    except Exception as e:
        print(f"Ошибка при получении данных: {e}")
        return []


def save_to_database(companies):
    """Сохраняет компании в базу данных"""
    conn = sqlite3.connect('stocks_bot.db')
    cursor = conn.cursor()

    # Очищаем таблицу перед добавлением новых данных
    cursor.execute("DELETE FROM companies")

    # Вставляем новые данные
    cursor.executemany("INSERT INTO companies (ticker, name) VALUES (?, ?)", companies)

    conn.commit()
    conn.close()
    print(f"Добавлено {len(companies)} компаний в базу данных")
if __name__ == "__main__":
    main()
import requests
import pandas as pd
from datetime import datetime, timedelta
import json


def get_moex_history_data(ticker, start_date, end_date):
    """
    Получает исторические данные по акции с Московской биржи
    :param ticker: Тикер акции (например, 'SBER')
    :param start_date: Начальная дата в формате 'YYYY-MM-DD'
    :param end_date: Конечная дата в формате 'YYYY-MM-DD'
    :return: DataFrame с данными
    """
    base_url = "https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/"
    url = f"{base_url}{ticker}.json?from={start_date}&till={end_date}"
    print(url)
    response = requests.get(url)
    data = response.json()
    # Извлекаем колонки и данные
    columns = data['history']['columns']
    rows = data['history']['data']

    df = pd.DataFrame(rows, columns=columns)
    return df


def save_to_csv(df, filename):
    """
    Сохраняет DataFrame в CSV файл
    :param df: DataFrame с данными
    :param filename: Имя файла для сохранения
    """
    columns_map = {
        'TRADEDATE': 'Date',
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'VOLUME': 'Volume',
        'VALUE': 'Value'
    }
    # for i in df:
    #     print(i)
    df = df[columns_map.keys()].rename(columns=columns_map)

    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Данные сохранены в файл: {filename}")





if __name__ == "__main__":
    # Параметры запроса
    TICKER = "SBER"  # Тикер акции
    END_DATE = datetime.now().strftime('%Y-%m-%d')  # Сегодняшняя дата
    START_DATE = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')  # Год назад

    # Получаем данные
    print(f"Запрашиваю данные для {TICKER} с {START_DATE} по {END_DATE}...")
    df = get_moex_history_data(TICKER, START_DATE, END_DATE)

    if df.empty:
        print("Не удалось получить данные. Проверьте тикер и даты.")
    else:
        # Оставляем только нужные колонки и переименовываем их


        # Сохраняем в CSV
        csv_filename = f"{TICKER}_{START_DATE}_{END_DATE}.csv"
        save_to_csv(df, csv_filename)

        # Выводим первые 5 строк для проверки
        print("\nПервые 5 строк данных:")
        print(df.head())
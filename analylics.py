import json
import pandas as pd

from get_graphs import save_to_csv, get_moex_history_data
from pathlib import Path
from PIL_drawer import PIL_drawer
from datetime import timedelta, datetime
from graphic import read_all_data, EMA, Zero, find_optimal_EMA, oper_MACD, MACD, Graphic, return_it_self
import os
import shutil

def get_history(ticker):
    end_date = datetime.now()  # Сегодняшняя дата
    start_date = (datetime.now() - timedelta(days=365))
    # Год назад
    d = {}
    with open(f"data/{ticker}/{ticker}_info", encoding='utf-8') as f:
        d = json.load(f)
    if d.get("last_update_data", 0) == end_date.strftime('%Y-%m-%d'):
        return True
    dataframes = []
    temp_date = start_date + timedelta(99)
    while end_date > temp_date:
        dataframes.append(get_moex_history_data(ticker, start_date.strftime('%Y-%m-%d'), temp_date.strftime('%Y-%m-%d')))
        start_date += timedelta(100)
        temp_date = start_date + timedelta(99)

    dataframes.append(get_moex_history_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    df = pd.concat(dataframes, axis=0)
    save_to_csv(df, f"data\\{ticker}\\{ticker}.csv")
    d["last_update_data"] = end_date.strftime('%Y-%m-%d')
    with open(f"data\\{ticker}\\{ticker}_info", "w",encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)
    print(f"Обновленна история для {ticker}")
    return True

def create_analytics(ticker):
    file_path = Path(f"data/{ticker}/{ticker}_info")
    if not file_path.exists():
        # Создаём директорию (если её нет) и записываем текст в файл
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Создать папки, если их нет
        file_path.write_text("{}")
    if not get_history(ticker):
        assert Exception
    d = {}

    with open(f"data/{ticker}/{ticker}_info", encoding='utf-8') as f:
        d = json.load(f)
    if d.get("last_update_analytics", 0) == d.get("last_update_data", -1):
        return True
    closes, highs, lows, opens = read_all_data(f"data/{ticker}/{ticker}.csv")
    if len(closes) == 0:
        if os.path.exists(f"data/{ticker}/"):
            shutil.rmtree(f"data/{ticker}/")  # или os.rmdir(path), если директория пуста
        else:
            print("Директория не существует!")
        print("Не существующий тикер")
        return False

    zero = Zero(len(closes))


    ft, sc = find_optimal_EMA(closes)
    macd = MACD(sc, ft)
    MACD_oper = oper_MACD(macd, EMA, 48)
    text = []
    for i in ft, sc, MACD_oper:
        text.append(f"{i} stonks {i.stonks} with chance {i.reliability}")
    if macd.line[-1] > 0:
        text.append(f"{macd} stonks")
    else:
        text.append(f"{macd} not stonks")
    for i in ft, sc, MACD_oper, macd:
        if i.signal:
            text.append(f"{i} signal!!!!!")

    d["last_update_analytics"] = datetime.now().strftime('%Y-%m-%d')
    print("\n".join(text))
    d["analytics"] = "\n".join(text)

    with open(f"data/{ticker}/{ticker}_info", "w", encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

    drawer = PIL_drawer()
    drawer.add((closes, highs, lows, opens))
    drawer.add(zero, (100, 100, 200))
    drawer.add(ft)
    drawer.add(sc)
    drawer.add(macd, (159, 129, 112))
    drawer.add(MACD_oper, (150, 10, 150))
    drawer.draw(f"data/{ticker}/{ticker}.png")

    print(f"Аналитика на {ticker} сделана")
    return True
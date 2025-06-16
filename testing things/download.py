import yfinance as yf

# Загрузка данных по акции (например, Apple)
data = yf.download("NFLX", start="2024-06-11", end="2025-11-06")

# Сохранение в CSV
data.to_csv("NFLX.csv")
print("Данные сохранены в NFLXcsv")
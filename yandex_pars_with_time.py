import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

# Создать подключение к базе данных
conn = sqlite3.connect('mydatabase.db')

# Создать DataFrame из SQL-таблицы с координатами клиента и офиса
query = "SELECT customer_latitude, customer_longitude, office_latitude, office_longitude FROM mytable"
df = pd.read_sql(query, conn)

# Использовать парсинг страницы Яндекс.Карт для вычисления расстояния между координатами
distances = []
for i in range(len(df)):
    customer_coords = f"{df['customer_longitude'][i]},{df['customer_latitude'][i]}"
    office_coords = f"{df['office_longitude'][i]},{df['office_latitude'][i]}"
    url = f"https://yandex.ru/maps/?ll={customer_coords}&mode=routes&rtext={office_coords}&rtt=comparison&z=14"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    distance_text = soup.find_all('span', {'class': 'route-snippet-view__distance-value'})[0].text
    distance = float(distance_text.replace(",", ".").replace("км", "").strip())
    distances.append(distance)
    time.sleep(0.5) # задержка на 0.5 секунды

# Добавить столбец с расстояниями в DataFrame
df['distance_km'] = distances

# Найти минимальное расстояние
min_distance = df['distance_km'].min()

# Найти индекс строки с минимальным расстоянием
min_distance_index = df['distance_km'].idxmin()

# Получить координаты клиента и офиса с минимальным расстоянием
min_distance_coords = [(df['customer_latitude'][min_distance_index], df['customer_longitude'][min_distance_index]),
                       (df['office_latitude'][min_distance_index], df['office_longitude'][min_distance_index])]

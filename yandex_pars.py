import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import sqlite3

# Создать подключение к базе данных
conn = sqlite3.connect('mydatabase.db')

# Создать DataFrame из SQL-таблицы с координатами клиента и офиса
query = "SELECT customer_latitude, customer_longitude, office_latitude, office_longitude FROM mytable"
df = pd.read_sql(query, conn)

# Определить URL-адрес страницы для получения расстояния
url = "https://yandex.ru/maps/?ll=37.312342%2C55.875415&mode=routes&rtext=&rtt=comparison&z=14"
params = {'rtext': f"{df['customer_latitude'][0]},{df['customer_longitude'][0]}~{df['office_latitude'][0]},{df['office_longitude'][0]}"}

# Отправить GET-запрос на страницу
response = requests.get(url, params=params)

# Получить HTML-код страницы
soup = BeautifulSoup(response.content, 'html.parser')

# Найти блок с расстоянием
distance_block = soup.find('span', class_='route-panel-view__info-text')

# Извлечь текст расстояния из блока и преобразовать в число
distance_str = distance_block.text.strip()
distance = float(re.search(r'\d+[\.\d]*', distance_str).group())

# Добавить столбец с расстоянием в DataFrame
df['distance_km'] = distance

# Найти минимальное расстояние
min_distance = df['distance_km'].min()

# Найти индекс строки с минимальным расстоянием
min_distance_index = df['distance_km'].idxmin()

# Получить координаты клиента и офиса с минимальным расстоянием
min_distance_coords = [(df['customer_latitude'][min_distance_index], df['customer_longitude'][min_distance_index]),
                       (df['office_latitude'][min_distance_index], df['office_longitude'][min_distance_index])]

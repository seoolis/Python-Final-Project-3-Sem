import pandas as pd
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# Список валют для учета
CURRENCY_CODES = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]

# Диапазон дат
START_DATE = datetime(2003, 1, 1)
END_DATE = datetime(2024, 11, 1)

# Путь для сохранения файла
OUTPUT_FILE = "D:/Project/Python/django-web-app/project/currency.csv"

# URL для получения данных
BASE_URL = "http://www.cbr.ru/scripts/XML_daily.asp"

# Функция для получения данных валют
def get_currency_data(date_str):
    url = f"{BASE_URL}?date_req={date_str}"
    response = requests.get(url)

    # Если запрос не удался
    if response.status_code != 200:
        return None

    try:
        # Парсим XML ответ
        root = ET.fromstring(response.content)

        # Извлекаем валюты, которые нас интересуют
        data = [
            {
                "CharCode": valute.find("CharCode").text,
                "Nominal": int(valute.find("Nominal").text),
                "Value": float(valute.find("Value").text.replace(",", "."))
            }
            for valute in root.findall(".//Valute")
            if valute.find("CharCode").text in CURRENCY_CODES
        ]

        if not data:
            return None

        # Создаем DataFrame для вычислений
        df = pd.DataFrame(data)

        # Расчет курса единицы валюты
        df['VunitRate'] = df.apply(lambda row: round(float(row['Value']) / int(row['Nominal']), 9), axis=1)

        # Создаем словарь для сохранения данных
        vunit_rate_dict = dict(zip(df['CharCode'], df['VunitRate']))
        vunit_rate_dict['date'] = datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m")

        # Заполняем отсутствующие валюты None
        for code in CURRENCY_CODES:
            vunit_rate_dict.setdefault(code, None)

        return vunit_rate_dict

    except Exception as e:
        print(f"Ошибка при обработке данных для {date_str}: {e}")
        return None

# Основная функция
def main():
    # Генерация всех дат первого числа месяца в указанном диапазоне
    all_dates = pd.date_range(start=START_DATE, end=END_DATE, freq='MS')
    all_data = []

    # Получаем данные по каждой дате
    for date in all_dates:
        date_str = date.strftime("%d/%m/%Y")
        currency_data = get_currency_data(date_str)

        if currency_data:
            all_data.append(currency_data)

    # Создание DataFrame из собранных данных
    df = pd.DataFrame(all_data)

    # Устанавливаем порядок столбцов, добавляем валюты
    df = df[['date'] + CURRENCY_CODES]

    # Сохраняем DataFrame в CSV файл
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Данные успешно сохранены в файл {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

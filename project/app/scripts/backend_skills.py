import pandas as pd
import csv
from collections import Counter

# Функция для сохранения данных в CSV файл
def save_skills_to_csv(filename, year, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['Year', 'Skill', 'Count'])  # Заголовки колонок
        for skill, count in data.items():
            writer.writerow([year, skill, count])  # Добавляем год в строку

# Основная функция
def run():
    # Создание словаря для хранения данных по годам
    skills_all_by_year = {year: [] for year in range(2015, 2025)}

    # Загрузка данных из CSV файла с pandas
    df = pd.read_csv('D:/Project/Python/django-web-app/project/table.csv', delimiter='|')

    # Преобразование строки в datetime с учетом часовых поясов
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True, errors='coerce')

    # Извлекаем год из столбца 'published_at'
    df['year'] = df['published_at'].dt.year

    # Процесс парсинга каждого навыка и подсчета упоминаний
    for _, row in df.iterrows():
        year = row['year']

        # Проверяем, что год в нужном диапазоне
        if 2015 <= year <= 2024:
            skills = row['key_skills'].split(';')  # Разделяем навыки по точке с запятой

            # Очистка и разделение навыков
            skills = [skill.strip() for skill in skills if skill.strip() != 'Нет данных']

            # Добавление навыков в соответствующий год
            skills_all_by_year[year].extend(skills)

    # Подсчет количества навыков по годам и сохранение в CSV файлы
    for year, skills in skills_all_by_year.items():
        if skills:  # Проверяем, что для данного года есть данные
            skills_count = Counter(skills)
            # Сохранение результата в CSV для каждого года
            save_skills_to_csv(f'D:/Project/Python/django-web-app/project/csv_files2/skills_{year}.csv', year, skills_count)

    print("Успешно")

# Запуск функции
run()
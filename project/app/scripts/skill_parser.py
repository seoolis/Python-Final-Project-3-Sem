#Выводит все скиллы по разделителю: Год, Навык, Количество упоминаний

import pandas as pd
import csv
from collections import Counter

def save_skills_to_csv(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['Year', 'Skill', 'Count'])
        for year, skills_count in data.items():
            for skill, count in skills_count.items():
                writer.writerow([year, skill, count])

def run():
    skills_all_by_year = {}

    # Загрузка данных из CSV файла с pandas
    df = pd.read_csv('D:/Project/Python/django-web-app/project/table.csv', delimiter='|')

    # Преобразование строки в datetime с учетом часовых поясов
    df['published_at'] = pd.to_datetime(df['published_at'], utc=True, errors='coerce')

    # Извлекаем год из столбца 'published_at'
    df['year'] = df['published_at'].dt.year

    # Процесс парсинга каждого навыка и подсчета упоминаний
    for _, row in df.iterrows():
        year = row['year']
        skills = row['key_skills'].split(';')  # Разделяем навыки по точке с запятой

        # Очистка и разделение навыков
        skills = [skill.strip() for skill in skills if skill.strip() != 'Нет данных']

        # Проверка наличия года в словаре, инициализация списка при необходимости
        if year in skills_all_by_year:
            skills_all_by_year[year].extend(skills)
        else:
            skills_all_by_year[year] = skills

    # Подсчет количества навыков по годам
    for year, skills in skills_all_by_year.items():
        skills_count = Counter(skills)
        # Сохранение результата в CSV
        save_skills_to_csv(f'D:/Project/Python/django-web-app/project/skill_parser_{year}.csv', {year: skills_count})

    print("Успешно")

# Запуск функции
run()
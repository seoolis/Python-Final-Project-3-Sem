#Скрипт вычисляет количество БЭКЕНД вакансий за год.

import pandas as pd

# Чтение данных из исходного файла test.csv
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/test.csv', encoding='utf-8', sep=',')

# Ключевые слова для поиска вакансий, связанных с backend
backend_keywords = ['backend', 'бэкэнд', 'бэкенд', 'back end', 'бэк энд', 'бэк енд']

# Фильтрация вакансий, которые содержат ключевые слова в названии
backend_vacancies = vacancies[vacancies['name'].str.contains('|'.join(backend_keywords), case=False, na=False)].copy()

# Использование .loc для добавления столбца 'year'
backend_vacancies.loc[:, 'year'] = backend_vacancies['published_at'].str[:4]

# Группировка по году и подсчет количества вакансий
vacancy_count_per_year = backend_vacancies.groupby('year').size().reset_index(name='count')

# Сохранение в новый CSV файл с нужными данными
vacancy_count_per_year.to_csv('D:/Project/Python/django-web-app/project/backend_vacancy.csv', index=False)

print("Новый файл успешно создан: backend_vacancy.csv")

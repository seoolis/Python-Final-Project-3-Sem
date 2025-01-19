import pandas as pd

# Чтение данных из исходного файла test.csv
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/test.csv', encoding='utf-8', sep=',')

# Извлечение года из столбца 'published_at' (формат 2003-01-31T18:24:11+03:00)
vacancies['year'] = vacancies['published_at'].str[:4]

# Группировка по году и подсчет общего количества вакансий (включая повторяющиеся)
total_vacancy_count_per_year = vacancies.groupby('year').size().reset_index(name='общее_количество_вакансий')

# Сохранение в новый CSV файл с нужными данными
total_vacancy_count_per_year.to_csv('D:/Project/Python/django-web-app/project/all_vacancy_by_year.csv', index=False)

print("Новый файл успешно создан: all_vacancy_by_year.csv")

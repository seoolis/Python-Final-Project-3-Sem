import pandas as pd
import numpy as np  # Добавляем numpy для явного использования np.nan

# Чтение данных из исходного файла test.csv
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/test.csv', encoding='utf-8', sep=',')

# Проверка столбцов
print("Имеющиеся столбцы в файле:", vacancies.columns)

# Ключевые слова для поиска вакансий, связанных с backend
backend_keywords = ['backend', 'бэкэнд', 'бэкенд', 'back end', 'бэк энд', 'бэк енд']

# Фильтрация вакансий, которые содержат ключевые слова в названии
backend_vacancies = vacancies[vacancies['name'].str.contains('|'.join(backend_keywords), case=False, na=False)]

# Создание нового DataFrame с необходимыми полями
formatted_vacancies = backend_vacancies[[
    'name', 'salary', 'area_name', 'published_at'
]].copy()

# Убедимся, что 'published_at' имеет корректный формат даты с учетом часовых поясов
formatted_vacancies['published_at'] = pd.to_datetime(
    formatted_vacancies['published_at'], errors='coerce', utc=True
)

# Обработка пустых значений (замена NaN на np.nan для единообразия)
formatted_vacancies['name'] = formatted_vacancies['name'].fillna(np.nan)
formatted_vacancies['salary'] = formatted_vacancies['salary'].fillna(np.nan)
formatted_vacancies['area_name'] = formatted_vacancies['area_name'].fillna(np.nan)
formatted_vacancies['published_at'] = formatted_vacancies['published_at'].fillna(np.nan)

# Сохранение отформатированного DataFrame в CSV файл
formatted_vacancies.to_csv('D:/Project/Python/django-web-app/project/backend_formatted_vacancy.csv', index=False, encoding='utf-8')

print("Новый файл успешно создан: backend_formatted_vacancy.csv")

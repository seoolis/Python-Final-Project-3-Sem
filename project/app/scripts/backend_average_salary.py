import pandas as pd

# Чтение данных из исходного файла test.csv
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/test.csv', encoding='utf-8', sep=',')

# Проверка столбцов
print(vacancies.columns)

# Ключевые слова для поиска вакансий, связанных с backend
backend_keywords = ['backend', 'бэкэнд', 'бэкенд', 'back end', 'бэк энд', 'бэк енд']

# Фильтрация вакансий, которые содержат ключевые слова в названии
backend_vacancies = vacancies[vacancies['name'].str.contains('|'.join(backend_keywords), case=False, na=False)]

# Использование .loc для преобразования столбца 'salary' в числовой формат
backend_vacancies.loc[:, 'salary'] = pd.to_numeric(backend_vacancies['salary'], errors='coerce')

# Сохранение в новый CSV файл с нужными данными: только name и salary
backend_vacancies[['name', 'salary']].to_csv('D:/Project/Python/django-web-app/project/backend_average_salary.csv', index=False)

print("Новый файл успешно создан: backend_average_salary.csv")

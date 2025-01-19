import csv
import os
from .models import Vacancy

# Указываем корневую директорию проекта
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Функция импорта данных в модель Vacancy
def import_vacancy_data():
    csv_file_path = os.path.join(project_root, 'test.csv')  # Путь к файлу vacancies.csv
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)  # Используем DictReader для чтения CSV с заголовками
        for row in reader:
            # Создаём объект Vacancy для каждой строки
            Vacancy.objects.create(
                name=row['Название вакансии'],  # Поле name
                key_skills=row['Ключевые навыки'],  # Поле key_skills
                salary_from=float(row['Зарплата от']) if row['Зарплата от'] else None,  # salary_from
                salary_to=float(row['Зарплата до']) if row['Зарплата до'] else None,  # salary_to
                salary_currency=row['Валюта'],  # salary_currency
                area_name=row['Город'],  # area_name
                published_at=row['Дата публикации']  # published_at
            )

# Основная функция для запуска импорта
def run():
    import_vacancy_data()
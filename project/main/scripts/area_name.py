import pandas as pd

# Чтение данных из test.csv
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/test.csv', encoding='utf-8', sep=',')

# Проверка доступных столбцов
print("Столбцы в файле:", vacancies.columns)

# Убедимся, что столбец 'salary' существует
if 'salary' not in vacancies.columns:
    print("Ошибка: столбец 'salary' отсутствует в данных.")
    exit()

# Извлечение года из столбца 'published_at' (формат 2003-01-31T18:24:11+03:00)
vacancies['year'] = vacancies['published_at'].str[:4]

# Группировка по году и городу: подсчет количества вакансий и средней зарплаты
vacancy_stats = vacancies.groupby(['year', 'area_name']).agg(
    количество_вакансий=('salary', 'size'),
    средняя_зарплата=('salary', 'mean')
).reset_index()

# Сохранение результата в новый CSV файл
vacancy_stats.to_csv('D:/Project/Python/django-web-app/project/vacancy_stats_by_year_and_city.csv', index=False)

print("Новый файл успешно создан: vacancy_stats_by_year_and_city.csv")

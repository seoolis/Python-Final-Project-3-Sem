import pandas as pd

# Загрузить CSV
df = pd.read_csv('D:/Project/Python/django-web-app/project/backend_avg_salary_by_year.csv')

# Преобразовать столбец "Средняя з/п для бэка"
df['Средняя з/п для бэка'] = df['Средняя з/п для бэка'].round(0).astype(int)

# Сохранить обновленный CSV
df.to_csv('D:/Project/Python/django-web-app/project/backend_avg_salary_by_year_updated.csv', index=False)

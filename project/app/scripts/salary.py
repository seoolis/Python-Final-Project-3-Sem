import pandas as pd
import psycopg2
import re


def calculate_average_salary(row):
    # Преобразуем зарплаты в числа, игнорируя ошибки
    salary_from = pd.to_numeric(row['salary_from'], errors='coerce')
    salary_to = pd.to_numeric(row['salary_to'], errors='coerce')

    # Если обе зарплаты отсутствуют, возвращаем NaN
    if pd.isna(salary_from) and pd.isna(salary_to):
        return pd.NA

    # Если одна из зарплат отсутствует, используем другую
    if pd.isna(salary_from):
        return salary_to
    if pd.isna(salary_to):
        return salary_from

    # Вычисление средней зарплаты
    return (salary_from + salary_to) / 2  # Можно использовать обычное деление, так как результат будет float


def extract_month_from_date(date_string):
    match = re.search(r'\d{4}-\d{2}', date_string)
    return match.group(0) if match else None

def adjust_published_date_format(date_string):
    return re.sub(r'(\+\d{2})(\d{2})$', r'\1:\2', date_string)


def convert_salary_to_rub(salary, currency, published_at, conn, currency_table):
    if currency not in ['BYR', 'USD', 'EUR', 'KZT', 'UAH', 'AZN', 'KGS', 'UZS']:
        return salary
    month = extract_month_from_date(published_at)
    if not month:
        return pd.NA
    query = f"SELECT {currency} FROM {currency_table} WHERE date = %s"
    cursor = conn.cursor()
    cursor.execute(query, (month,))
    result = cursor.fetchone()
    cursor.close()

    if result and result[0] is not None:
        # Преобразуем Decimal в float перед умножением
        return salary * float(result[0])

    return pd.NA


# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    dbname="vacancies_2024",
    user="postgres",  # Укажите ваш пользователь в PostgreSQL
    password="123",  # Укажите ваш пароль
    host="localhost",  # Или IP-адрес вашего сервера PostgreSQL
    port="5432"
)

# Чтение данных из CSV
vacancies = pd.read_csv('D:/Project/Python/django-web-app/project/table.csv', encoding='utf-8', sep='|')

# Заполнение пропусков в зарплатах
vacancies['salary_from'] = vacancies['salary_from'].fillna(vacancies['salary_to'])
vacancies['salary_to'] = vacancies['salary_to'].fillna(vacancies['salary_from'])

# Вычисление средней зарплаты
vacancies['salary'] = vacancies.apply(calculate_average_salary, axis=1)

# Конвертация зарплаты в рубли
for index, row in vacancies.iterrows():
    converted_salary = convert_salary_to_rub(
        row['salary'], row['salary_currency'], row['published_at'], conn, 'currency_table'
    )
    vacancies.at[index, 'salary'] = int(converted_salary) if pd.notna(converted_salary) else pd.NA
    vacancies.at[index, 'published_at'] = adjust_published_date_format(row['published_at'])

# Сохранение данных в файл test.csv
final_vacancies = vacancies[['name', 'salary', 'area_name', 'published_at']]
final_vacancies.to_csv('D:/Project/Python/django-web-app/project/test.csv', index=False)

# Закрытие подключения к базе данных
conn.close()


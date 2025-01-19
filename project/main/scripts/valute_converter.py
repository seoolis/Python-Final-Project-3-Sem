import pandas as pd
import psycopg2
import re

def calculate_average_salary(row):
    if pd.isna(row['salary_from']) and pd.isna(row['salary_to']):
        return pd.NA
    if pd.isna(row['salary_from']):
        return row['salary_to']
    if pd.isna(row['salary_to']):
        return row['salary_from']
    return (row['salary_from'] + row['salary_to']) // 2

def extract_month_from_date(date_string):
    match = re.search(r'\d{4}-\d{2}', date_string)
    return match.group(0) if match else None

def adjust_published_date_format(date_string):
    return re.sub(r'(\+\d{2})(\d{2})\$', r'\1:\2', date_string)

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
        return salary * result[0]
    return pd.NA

# Input parameters
database_name = 'vacancies_2024'
user = 'postgres'
password = '123'
host = 'localhost'
port = '5432'
csv_file = 'D:/Project/Python/django-web-app/project/table.csv'
table_name = 'vacancy_table'
currency_table = 'currency_table'

conn = psycopg2.connect(
    dbname=database_name,
    user=user,
    password=password,
    host=host,
    port=port
)

try:
    vacancies = pd.read_csv(csv_file, encoding='utf-8', delimiter='|', on_bad_lines='skip')
except pd.errors.ParserError as e:
    print(f"Error parsing CSV file: {e}")
    exit(1)

vacancies['salary_from'] = vacancies['salary_from'].fillna(vacancies['salary_to'])
vacancies['salary_to'] = vacancies['salary_to'].fillna(vacancies['salary_from'])

vacancies['salary'] = vacancies.apply(calculate_average_salary, axis=1)

for index, row in vacancies.iterrows():
    converted_salary = convert_salary_to_rub(
        row['salary'], row['salary_currency'], row['published_at'], conn, currency_table
    )
    vacancies.at[index, 'salary'] = int(converted_salary) if pd.notna(converted_salary) else pd.NA
    vacancies.at[index, 'published_at'] = adjust_published_date_format(row['published_at'])


final_vacancies = vacancies[['name', 'salary', 'area_name', 'published_at']]

create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    name TEXT,
    salary INTEGER,
    area_name TEXT,
    published_at TEXT
);
"""

cursor = conn.cursor()
cursor.execute(create_table_query)
conn.commit()
cursor.close()

# Insert data into the table
from sqlalchemy import create_engine

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}')
final_vacancies.to_sql(table_name, engine, if_exists='replace', index=False, dtype={'salary': 'INTEGER'})

# Close the connection
conn.close()
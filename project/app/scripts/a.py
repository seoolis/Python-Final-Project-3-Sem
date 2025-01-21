import psycopg2
import csv

# Параметры подключения к базе данных
db_params = {
    'dbname': 'backend',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',  # например, localhost или IP
    'port': '5432',  # обычно 5432
}

# SQL-запрос для выборки уровня зарплат по городам для Backend
sql_query = """
    SELECT
        area_name AS "Город",
        ROUND(AVG(CAST(salary AS FLOAT))::numeric, 2) AS "Уровень зарплат по городам"
    FROM all_formatted_vacancies
    WHERE
        (name LIKE '%backend%'
        OR name LIKE '%Backend-программист%'
        OR name LIKE '%бэкэнд%'
        OR name LIKE '%бэкенд%'
        OR name LIKE '%бекенд%'
        OR name LIKE '%бекэнд%'
        OR name LIKE '%back end%'
        OR name LIKE '%бэк энд%'
        OR name LIKE '%бэк енд%'
        OR name LIKE '%django%'
        OR name LIKE '%flask%'
        OR name LIKE '%laravel%'
        OR name LIKE '%yii%'
        OR name LIKE '%symfony%')
    AND salary ~ '^\d+(\.\d+)?$'  -- Это условие фильтрует только строки, где salary - корректное число (целое или с плавающей запятой)
    GROUP BY area_name
    ORDER BY ROUND(AVG(CAST(salary AS FLOAT))::numeric, 2) DESC
    LIMIT 15
"""


# Функция для выполнения запроса и записи результата в CSV
def fetch_and_save_to_csv():
    try:
        # Подключаемся к базе данных PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Выполняем SQL-запрос
        cursor.execute(sql_query)

        # Получаем все строки результата запроса
        rows = cursor.fetchall()

        # Открываем CSV файл для записи
        with open('backend_salary_2.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Записываем заголовки
            writer.writerow(["Город", "Уровень зарплат по городам"])

            # Записываем строки данных
            writer.writerows(rows)

        print("Данные успешно сохранены в файл backend_salary_2.csv")

    except Exception as e:
        print(f"Ошибка: {e}")

    finally:
        # Закрываем соединение с базой данных
        cursor.close()
        conn.close()

# Вызов функции для получения данных и записи в CSV
fetch_and_save_to_csv()

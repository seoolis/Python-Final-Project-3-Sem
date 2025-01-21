import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="backend",  # Убедитесь, что это имя вашей базы данных
    user="postgres",   # Ваш пользователь PostgreSQL
    password="123",    # Ваш пароль
    host="localhost",  # Или другой адрес
    port="5432"        # Порт по умолчанию для PostgreSQL
)

try:
    with conn.cursor() as cur:
        # Запрос для уровня зарплат по городам
        cur.execute("""
            SELECT
                area_name AS "Город",
                ROUND(AVG(CAST(salary AS NUMERIC)), 2) AS "Уровень зарплат по городам"
            FROM all_formatted_vacancies
            WHERE
                (name LIKE '%backend%' OR 
                name LIKE '%Backend-программист%' OR 
                name LIKE '%бэкэнд%' OR 
                name LIKE '%бэкенд%' OR 
                name LIKE '%бекенд%' OR 
                name LIKE '%бекэнд%' OR 
                name LIKE '%back end%' OR 
                name LIKE '%бэк энд%' OR 
                name LIKE '%бэк енд%' OR 
                name LIKE '%django%' OR 
                name LIKE '%flask%' OR 
                name LIKE '%laravel%' OR 
                name LIKE '%yii%' OR 
                name LIKE '%symfony%')
                AND salary IS NOT NULL
                AND salary <> ''
                AND salary ~ '^[0-9]+(\.[0-9]+)?$'  -- Регулярное выражение для проверки числовых значений
            GROUP BY area_name
            ORDER BY ROUND(AVG(CAST(salary AS NUMERIC)), 2) DESC
            LIMIT 15;
        """)
        salary_area_data = cur.fetchall()

        # Запись в CSV
        with open("../../salary.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Город", "Уровень зарплат по городам"])  # Заголовки
            writer.writerows(salary_area_data)
        print("Данные для уровня зарплат по городам записаны в файл salary.csv")

        # Запрос для доли вакансий по городам
        cur.execute("""
            SELECT
                area_name AS "Город",
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 2) AS "Доля вакансий в %"
            FROM vacancies
            GROUP BY area_name
            ORDER BY COUNT(*) DESC
            LIMIT 15;
        """)
        dolya_area_data = cur.fetchall()

        # Запись в CSV
        with open("../../part_area.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Город", "Доля вакансий в %"])  # Заголовки
            writer.writerows(dolya_area_data)
        print("Данные для доли вакансий по городам записаны в файл part_area.csv")

        # Запрос для уровня зарплат по городам для бэкендера
        cur.execute("""
            SELECT
                area_name AS "Город",
                ROUND(AVG(CAST(salary AS NUMERIC)), 2) AS "Уровень зарплат по городам"
            FROM all_formatted_vacancies
            WHERE
                name LIKE '%backend%' OR name LIKE '%Backend-программист%' OR name LIKE '%бэкэнд%' OR
                name LIKE '%бэкенд%' OR name LIKE '%бекенд%' OR name LIKE '%бекэнд%' OR name LIKE '%back end%' OR
                name LIKE '%бэк энд%' OR name LIKE '%бэк енд%' OR name LIKE '%django%' OR name LIKE '%flask%' OR
                name LIKE '%laravel%' OR name LIKE '%yii%' OR name LIKE '%symfony%'
            GROUP BY area_name
            ORDER BY ROUND(AVG(CAST(salary AS NUMERIC)), 2) DESC
            LIMIT 15;
        """)
        salary_area_backend_data = cur.fetchall()

        # Запись в CSV
        with open("../../salary_backend.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Город", "Уровень зарплат по городам"])  # Заголовки
            writer.writerows(salary_area_backend_data)
        print("Данные для уровня зарплат по городам для бэкендера записаны в файл salary_backend.csv")

        # Запрос для доли вакансий по городам для бэкендера
        cur.execute("""
            SELECT
                area_name AS "Город",
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM vacancies), 3) AS "Доля вакансий в %"
            FROM vacancies
            WHERE
                name LIKE '%backend%' OR name LIKE '%Backend-программист%' OR name LIKE '%бэкэнд%' OR
                name LIKE '%бэкенд%' OR name LIKE '%бекенд%' OR name LIKE '%бекэнд%' OR name LIKE '%back end%' OR
                name LIKE '%бэк энд%' OR name LIKE '%бэк енд%' OR name LIKE '%django%' OR name LIKE '%flask%' OR
                name LIKE '%laravel%' OR name LIKE '%yii%' OR name LIKE '%symfony%'
            GROUP BY area_name
            ORDER BY COUNT(*) DESC
            LIMIT 15;
        """)
        dolya_area_backend_data = cur.fetchall()

        # Запись в CSV
        with open("../../part_area_backend.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Город", "Доля вакансий в %"])  # Заголовки
            writer.writerows(dolya_area_backend_data)
        print("Данные для доли вакансий по городам для бэкендера записаны в файл part_area_backend.csv")

finally:
    conn.close()

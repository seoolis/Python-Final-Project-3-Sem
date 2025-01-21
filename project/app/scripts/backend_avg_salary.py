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
        # Запрос средней зарплаты для backend
        cur.execute("""
            SELECT
                SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) AS "Год",
                ROUND(AVG(CAST(salary AS NUMERIC)), 2) AS "Средняя з/п для бэка"
            FROM all_formatted_vacancies
            WHERE 
                name ILIKE '%backend%'
                OR name ILIKE '%Backend-программист%'
                OR name ILIKE '%бэкэнд%'
                OR name ILIKE '%бэкенд%'
                OR name ILIKE '%бекенд%'
                OR name ILIKE '%бекэнд%'
                OR name ILIKE '%back end%'
                OR name ILIKE '%бэк энд%'
                OR name ILIKE '%бэк енд%'
                OR name ILIKE '%django%'
                OR name ILIKE '%flask%'
                OR name ILIKE '%laravel%'
                OR name ILIKE '%yii%'
                OR name ILIKE '%symfony%'
            GROUP BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4)
            ORDER BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) DESC;
        """)
        backend_avg_salaries = cur.fetchall()

        # Создание CSV файла и запись результата
        with open("../../backend_avg_salary_by_year.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Заголовки
            writer.writerow(["Год", "Средняя з/п для бэка"])
            # Запись данных
            writer.writerows(backend_avg_salaries)
        print("Данные по средней зарплате для backend записаны в файл backend_avg_salary_by_year.csv")

finally:
    conn.close()

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
        # Первый запрос: количество вакансий по годам
        cur.execute("""
            SELECT
                SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) AS "Год",
                COUNT(*) AS "Количество вакансий"
            FROM vacancies
            GROUP BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4)
            ORDER BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) DESC
        """)
        vacancies = cur.fetchall()

        # Создание нового CSV файла и запись результата
        with open("../../vacancies_by_year.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Заголовки
            writer.writerow(["Год", "Количество вакансий"])
            # Запись данных
            writer.writerows(vacancies)
        print("Данные по количеству вакансий записаны в файл vacancies_by_year.csv")

        # Второй запрос: средняя зарплата по годам
        cur.execute("""
            SELECT
                SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) AS "Год",
                ROUND(AVG(CAST(salary AS NUMERIC)), 2) AS "Средняя з/п"
            FROM all_formatted_vacancies
            GROUP BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4)
            ORDER BY SUBSTRING(CAST(published_at AS TEXT) FROM 1 FOR 4) DESC
        """)
        avg_salaries = cur.fetchall()

        # Создание нового CSV файла и запись результата
        with open("../../avg_salary_by_year.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Заголовки
            writer.writerow(["Год", "Средняя з/п"])
            # Запись данных
            writer.writerows(avg_salaries)
        print("Данные по средней зарплате записаны в файл avg_salary_by_year.csv")

finally:
    conn.close()

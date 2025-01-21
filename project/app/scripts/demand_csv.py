import psycopg2

# Параметры подключения к PostgreSQL
conn = psycopg2.connect(
    dbname="backend",  # Убедитесь, что это имя вашей базы данных
    user="postgres",   # Ваш пользователь PostgreSQL
    password="123",    # Ваш пароль
    host="localhost",  # Или другой адрес
    port="5432"        # Порт по умолчанию для PostgreSQL
)

# Создание курсора для выполнения запроса
cur = conn.cursor()

# Новый SQL-запрос для вакансий с бекенд-разработчиками
backend_query = """
    SELECT
        EXTRACT(YEAR FROM published_at) AS "Год",
        COUNT(*) AS "Количество вакансий для бэка"
    FROM vacancies
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
    GROUP BY EXTRACT(YEAR FROM published_at)
    ORDER BY EXTRACT(YEAR FROM published_at) DESC
"""

# Выполнение запроса и экспорт данных в CSV
cur.execute(f"COPY ({backend_query}) TO 'D:/Project/Python/django-web-app/project/backend_vacancy_query.csv' WITH CSV HEADER;")

# Закрытие курсора и соединения
cur.close()
conn.close()

print("Экспорт завершен!")
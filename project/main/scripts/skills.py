import psycopg2
from collections import Counter
import csv


# Подключение к базе данных PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="vacancies_2024",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )


# Получение навыков по годам
def get_skills_by_year():
    try:
        # Устанавливаем соединение с базой данных
        conn = get_connection()
        cursor = conn.cursor()

        # Список ключевых слов для поиска backend-разработчиков
        profession_keywords = [
            'backend', 'бэкэнд', 'бэкенд', 'бекенд',
            'бекэнд', 'back end', 'бэк энд', 'бэк енд'
        ]

        # Формируем условие для SQL-запроса
        keywords_condition = " OR ".join(
            [f"name ILIKE '%{keyword}%'" for keyword in profession_keywords]
        )

        # SQL-запрос для извлечения данных по годам
        query = f"""
            SELECT 
                EXTRACT(YEAR FROM TO_DATE(published_at, 'YYYY-MM-DD')) AS year,
                key_skills
            FROM vacancy_table 
            WHERE {keywords_condition};
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Сортируем данные по годам
        data_by_year = {}
        for row in rows:
            year = int(row[0])  # Год
            key_skills = row[1]  # Навыки
            if year not in data_by_year:
                data_by_year[year] = []
            if key_skills:
                data_by_year[year].extend(
                    [skill.strip() for skill in key_skills.replace("\r", "").replace(",", ";").split(";") if skill.strip()]
                )

        # Подсчёт частоты навыков для каждого года
        skills_by_year = {}
        for year, skills in data_by_year.items():
            skills_counter = Counter(skills)
            skills_by_year[year] = skills_counter.most_common(20)  # ТОП-20 навыков

        return skills_by_year

    except Exception as e:
        print(f"Ошибка: {e}")
        return {}

    finally:
        if conn:
            cursor.close()
            conn.close()

# Запись результатов по годам в CSV-файл
def save_to_csv_by_year(skills_data, filename="skills_by_year.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="\t")  # Используем табуляцию как разделитель
            writer.writerow(["Год", "Навык", "Количество упоминаний"])  # Заголовки колонок

            for year, skills in skills_data.items():
                for skill, count in skills:
                    writer.writerow([year, skill, count])

        print(f"Результаты успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")

# Автоматическое выполнение
if __name__ == "__main__":
    skills_by_year = get_skills_by_year()
    if skills_by_year:
        save_to_csv_by_year(skills_by_year)
    else:
        print("Данные не найдены.")
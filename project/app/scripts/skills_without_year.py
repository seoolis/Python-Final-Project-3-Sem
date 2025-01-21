# Скрипт предназначен для того, чтобы извлечь популярные навыки только для профессии бэкендера.
# Извлекается без года. То есть это навыки бэкендера с общим кол-вом упоминания.
# Выводит: Навык, Количество упоминаний

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

# Получение ТОП-20 навыков для backend-разработчиков
def get_top_skills():
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

        # SQL-запрос для получения навыков
        query = f"""
            SELECT key_skills 
            FROM vacancy_table 
            WHERE {keywords_condition};
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Разбивка навыков и подсчёт частоты
        def split_skills(skill_data):
            if not skill_data:
                return []
            # Учитываем разные разделители: ';', ',', '\n'
            skills = [skill.strip() for skill in skill_data.replace("\r", "").replace(",", ";").split(";") if skill.strip()]
            # Фильтруем "нет данных"
            return [skill for skill in skills if "нет данных" not in skill.lower()]

        all_skills = []
        for row in rows:
            all_skills.extend(split_skills(row[0]))  # Разбиваем навыки и добавляем в общий список

        # Подсчёт частоты навыков
        skills_counter = Counter(all_skills)
        top_skills = skills_counter.most_common(20)  # ТОП-20 навыков

        return top_skills

    except Exception as e:
        print(f"Ошибка: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

# Запись в CSV-файл
def save_to_csv(skills_data, filename="top_20_skills_backend.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="|")  # Используем | как разделитель
            writer.writerow(["Навык", "Количество упоминаний"])  # Заголовки колонок
            writer.writerows(skills_data)
        print(f"Результаты успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")

# Автоматическое выполнение
if __name__ == "__main__":
    top_skills = get_top_skills()
    if top_skills:
        save_to_csv(top_skills)
    else:
        print("Данные не найдены.")
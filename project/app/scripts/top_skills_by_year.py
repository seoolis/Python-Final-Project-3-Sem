import psycopg2
from collections import Counter
import csv


# Подключение к базе данных PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="backend",
        user="postgres",
        password="123",
        host="localhost",
        port="5432"
    )


# Получение ТОП-20 навыков по годам для всех профессий
def get_top_skills_by_year():
    try:
        # Устанавливаем соединение с базой данных
        conn = get_connection()
        cursor = conn.cursor()

        # SQL-запрос для получения навыков и года
        query = """
            SELECT published_at, key_skills 
            FROM vacancies;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Разбивка навыков и подсчёт частоты
        def split_skills(skill_data):
            if not skill_data:
                return []
            # Учитываем разные разделители: ';', ',', '\n'
            skills = [skill.strip() for skill in skill_data.replace("\r", "").replace(",", ";").split(";") if
                      skill.strip()]
            # Фильтруем "нет данных"
            return [skill for skill in skills if "нет данных" not in skill.lower()]

        # Словарь для хранения всех навыков по годам
        year_skills = {}

        for row in rows:
            year = row[0]
            skills = split_skills(row[1])

            if year not in year_skills:
                year_skills[year] = []
            year_skills[year].extend(skills)

        # Подсчёт частоты навыков по годам
        top_skills_by_year = {}

        for year, skills in year_skills.items():
            skills_counter = Counter(skills)
            top_skills_by_year[year] = skills_counter.most_common(20)  # ТОП-20 навыков по году

        return top_skills_by_year

    except Exception as e:
        print(f"Ошибка: {e}")
        return {}

    finally:
        if conn:
            cursor.close()
            conn.close()


# Запись в CSV-файл
def save_to_csv(top_skills_by_year, filename="top_20_skills_by_year.csv"):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter="|")  # Используем | как разделитель
            writer.writerow(["Год", "Навык", "Количество упоминаний"])  # Заголовки колонок

            for year, skills in top_skills_by_year.items():
                for skill, count in skills:
                    writer.writerow([year, skill, count])

        print(f"Результаты успешно сохранены в файл: {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV: {e}")


# Автоматическое выполнение
if __name__ == "__main__":
    top_skills_by_year = get_top_skills_by_year()
    if top_skills_by_year:
        save_to_csv(top_skills_by_year)
    else:
        print("Данные не найдены.")

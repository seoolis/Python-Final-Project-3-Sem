import csv
from collections import Counter

def save_top_skills_to_csv(filename, data):
    """
    Сохраняет данные о топовых навыках в CSV-файл.

    :param filename: Имя выходного файла.
    :param data: Словарь с данными (год -> (навык, количество)).
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Year', 'Skill', 'Count'])
        for year, (skill, count) in data.items():
            writer.writerow([year, skill, count])

def run():
    """
    Анализирует файл CSV, группирует навыки по годам и находит самый популярный навык для каждого года.
    """
    skills_by_year = {}

    # Открываем CSV с указанием разделителя '|'
    with open('D:/Project/Python/django-web-app/project/table.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')  # Указан разделитель '|'

        for row in reader:
            # Проверяем наличие столбца 'published_at'
            if 'published_at' not in row:
                raise ValueError("Столбец 'published_at' отсутствует в файле.")

            year = row['published_at'][:4]  # Извлечение года из столбца published_at
            key_skills = row['key_skills']

            # Проверяем, есть ли навыки
            if key_skills == "Нет данных" or not key_skills.strip():
                continue

            # Разделяем навыки по разделителю `;`
            skills = key_skills.split(';')
            skills = [skill.strip() for skill in skills if skill.strip()]  # Удаляем пустые строки и пробелы

            # Добавляем навыки к соответствующему году
            if year in skills_by_year:
                skills_by_year[year].extend(skills)
            else:
                skills_by_year[year] = skills

    # Подсчёт всех навыков по годам и выбор самого частого навыка
    top_skills_by_year = {}
    for year, skills in skills_by_year.items():
        skills_count = Counter(skills)
        most_common_skill, count = skills_count.most_common(1)[0]  # Выбираем самый частый навык
        top_skills_by_year[year] = (most_common_skill, count)

    # Сохраняем результаты
    save_top_skills_to_csv('top_skills_by_year.csv', top_skills_by_year)
    print("Анализ завершен. Результаты сохранены в 'top_skills_by_year.csv'.")

if __name__ == "__main__":
    run()

import csv
import re
import os

def clean_value(value):
    value = re.sub(r'<[^>]+>', '', value)
    value = re.sub(r'\s+', ' ', value).strip()
    return value

def process_field(value):
    if not value.strip():
        return "Нет данных"
    parts = value.split('\n')
    cleaned_parts = [clean_value(part) for part in parts]
    return '; '.join(cleaned_parts)

# Исходный файл
input_file = 'D:/Project/Python/django-web-app/vacancies_2024.csv'

# Путь к выходному файлу
output_dir = 'main/scripts'
os.makedirs(output_dir, exist_ok=True)  # Создать папки, если их нет
output_file = os.path.join(output_dir, 'table.csv')

with open(input_file, encoding='utf-8-sig') as infile:
    reader = csv.reader(infile)
    headers = next(reader)

    # Отфильтровать строки с достаточным количеством заполненных полей
    rows = [row for row in reader if sum(1 for field in row if field.strip()) >= len(headers) / 2]

    # Обработка и запись в новый файл с разделителем |
    with open(output_file, mode='w', encoding='utf-8-sig', newline='') as outfile:
        writer = csv.writer(outfile, delimiter='|')
        writer.writerow(headers)  # Записать заголовки

        for row in rows:
            processed_row = [process_field(row[j]) for j in range(len(headers))]
            writer.writerow(processed_row)

print(f"Данные успешно записаны в файл: {output_file}")

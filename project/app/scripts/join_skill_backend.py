import pandas as pd
import glob

# Путь к папке с CSV файлами
path = 'D:/Project/Python/django-web-app/project/csv_files2/'

# Список всех файлов CSV в указанной папке
csv_files = glob.glob(path + "*.csv")

# Объединение всех CSV файлов в один DataFrame
combined_data = pd.concat(
    (pd.read_csv(file, encoding='utf-8', sep='|') for file in csv_files), ignore_index=True
)

# Проверка столбцов
print("Имеющиеся столбцы в объединенном файле:", combined_data.columns)

# Замена null или пустых значений в столбце Skill
combined_data['Skill'] = combined_data['Skill'].fillna('Unknown')

# Сохранение объединенного DataFrame в CSV файл
combined_data.to_csv('D:/Project/Python/django-web-app/project/all_backend_skills.csv', index=False, encoding='utf-8', sep='|')

print("Новый файл успешно создан: all_backend_skills.csv")

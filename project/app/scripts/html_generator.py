import pandas as pd

df = pd.read_csv('D:/Project/Python/django-web-app/project/backend_vacancy.csv')

df.to_html('backend_vacancy.html')
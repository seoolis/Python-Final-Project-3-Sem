#Скрипт предназначен для того, чтобы обновлять данные по валютам.

import pandas as pd
from .models import Currency

def save_currency_data_to_database():
    df = pd.read_csv('currency.csv')

    currency_data_list = df.to_dict(orient='records')

    for currency_data in currency_data_list:
        currency = Currency(date=currency_data.get('date'), byr=currency_data.get('BYR'), usd=currency_data.get('USD'),
                            eur=currency_data.get('EUR'), kzt=currency_data.get('KZT'),
                            uah=currency_data.get('UAH'), azn=currency_data.get('AZN'),
                            kgs=currency_data.get('KGS'), uzs=currency_data.get('UZS'),
                            gel=currency_data.get('GEL'))
        currency.save()

def run():
    save_currency_data_to_database()
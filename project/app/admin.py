from django.contrib import admin
from .models import Vacancy
from .models import Currency

class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at')
    search_fields = ['name', 'area_name']

    # Устанавливаем лимит на количество записей на странице
    list_per_page = 100

    # Фильтрация по валюте и городу
    list_filter = ['salary_currency', 'area_name']

    # Сортировка по полю id по возрастанию
    ordering = ['id']

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('date', 'byr', 'usd', 'eur', 'kzt', 'uah', 'azn', 'kgs', 'uzs', 'gel')
    search_fields = ['date']

admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Currency, CurrencyAdmin)
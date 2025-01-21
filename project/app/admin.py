from django.contrib import admin
from .models import Vacancy, FormattedVacancy, FormattedVacancyAll, SkillByYear, SkillsBackend, SkillsBackendByYear, \
    VacancyStatistic, BackendVacancyStatistic, AverageSalary, BackendAverageSalary, Salary, SalaryBackend, PartArea, \
    PartAreaBackend
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

class FormattedVacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary', 'area_name', 'published_at')

class AllFormattedVacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'salary', 'area_name', 'published_at')

class SkillByYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'year')

class SkillsBackendByYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'year')

class SkillsBackendAdmin(admin.ModelAdmin):
    list_display = ('name', 'count')

class VacancyStatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'vacancy_count')

class BackendVacancyStatisticAdmin(admin.ModelAdmin):
    list_display = ('year', 'vacancy_count')

class AverageSalaryAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary')

class BackendAverageSalaryAdmin(admin.ModelAdmin):
    list_display = ('year', 'salary')

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'average_salary')

class SalaryBackendAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'average_salary')

class PartAreaAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'percentage')

class PartAreaBackendAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'percentage')

admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(FormattedVacancy, FormattedVacancyAdmin)
admin.site.register(FormattedVacancyAll, AllFormattedVacancyAdmin)
admin.site.register(SkillByYear, SkillByYearAdmin)
admin.site.register(SkillsBackendByYear, SkillsBackendByYearAdmin)  # Регистрация SkillBackendByYear
admin.site.register(SkillsBackend, SkillsBackendAdmin)  # Регистрация SkillBackend
admin.site.register(VacancyStatistic, VacancyStatisticAdmin)
admin.site.register(BackendVacancyStatistic, BackendVacancyStatisticAdmin)
admin.site.register(AverageSalary, AverageSalaryAdmin)
admin.site.register(BackendAverageSalary, BackendAverageSalaryAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(SalaryBackend, SalaryBackendAdmin)
admin.site.register(PartArea, PartAreaAdmin)
admin.site.register(PartAreaBackend, PartAreaBackendAdmin)
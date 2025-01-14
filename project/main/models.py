from django.db import models

class Vacancy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название вакансии")
    key_skills = models.TextField(verbose_name="Ключевые навыки")
    salary_from = models.FloatField(null=True, blank=True, verbose_name="Зарплата от")
    salary_to = models.FloatField(null=True, blank=True, verbose_name="Зарплата до")
    salary_currency = models.CharField(max_length=10, verbose_name="Валюта")
    area_name = models.CharField(max_length=255, verbose_name="Город")
    published_at = models.DateField(verbose_name="Дата публикации")
from django.db import models

class Vacancy(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название вакансии")
    key_skills = models.TextField(verbose_name="Ключевые навыки")
    salary_from = models.FloatField(null=True, blank=True, verbose_name="Зарплата от")
    salary_to = models.FloatField(null=True, blank=True, verbose_name="Зарплата до")
    salary_currency = models.CharField(max_length=10, verbose_name="Валюта")
    area_name = models.CharField(max_length=255, verbose_name="Город")
    published_at = models.DateField(verbose_name="Дата публикации")

    class Meta:
        db_table = 'vacancy_table'

        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return f"{self.name}"

class Currency(models.Model):
    date = models.CharField(max_length=7)
    byr = models.FloatField(null=True, blank=True)
    usd = models.FloatField(null=True, blank=True)
    eur = models.FloatField(null=True, blank=True)
    kzt = models.FloatField(null=True, blank=True)
    uah = models.FloatField(null=True, blank=True)
    azn = models.FloatField(null=True, blank=True)
    kgs = models.FloatField(null=True, blank=True)
    uzs = models.FloatField(null=True, blank=True)
    gel = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.date}"

    class Meta:
        ordering = ['date']
        db_table = 'currency_table'

        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"
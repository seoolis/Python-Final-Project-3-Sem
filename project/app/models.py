from django.db import models

#Общее

class Vacancy(models.Model): #Все вакансии - стандартная таблица
    name = models.CharField(max_length=255, verbose_name="Название вакансии")
    key_skills = models.TextField(verbose_name="Ключевые навыки")
    salary_from = models.CharField(max_length=255, null=True, default=None)
    salary_to = models.CharField(max_length=255, null=True, default=None)
    salary_currency = models.CharField(max_length=10, verbose_name="Валюта")
    area_name = models.CharField(max_length=255, verbose_name="Город")
    published_at = models.DateField(verbose_name="Дата публикации")

    class Meta:
        db_table = 'vacancies'

        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"

    def __str__(self):
        return f"{self.name}"

class Currency(models.Model): #Валюта - стандартная таблица
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

class FormattedVacancy(models.Model): #Отформатированная таблица - со средней з/п Backend
    name = models.TextField(max_length=255, null=True, default=None)
    salary = models.CharField(max_length=255, null=True, default=None)
    area_name = models.TextField(null=True, default=None)
    published_at = models.DateTimeField(null=False, default=None)

    def __str__(self):
        return f"{self.name} {self.area_name} {self.published_at}"

    class Meta:
        db_table = 'formatted_vacancies'
        verbose_name = "Отформатированные вакансии"
        verbose_name_plural = "Отформатированные вакансии"

class FormattedVacancyAll(models.Model): #Отформатированная таблица - со средней з/п всех профессий
    name = models.TextField(max_length=255, null=True, default=None)
    salary = models.CharField(max_length=255, null=True, default=None)
    area_name = models.TextField(null=True, default=None)
    published_at = models.DateTimeField(null=False, default=None)

    def __str__(self):
        return f"{self.name} {self.area_name} {self.published_at}"

    class Meta:
        db_table = 'all_formatted_vacancies'
        verbose_name = "Все отформатированные вакансии"
        verbose_name_plural = "Все отформатированные вакансии"

#Навыки

class SkillsBackendByYear(models.Model): #Популярные навыки у бэкендера за разные года (ТОП-20)
    year = models.IntegerField()  # Год
    name = models.CharField(max_length=255)  # Название навыка
    count = models.IntegerField()  # Количество упоминаний

    def __str__(self):
        return self.name

class SkillsBackend(models.Model): #Популярные навыки у бэкендера
    name = models.CharField(max_length=255)  # Название навыка
    count = models.IntegerField()  # Количество упоминаний

    def __str__(self):
        return self.name

class SkillByYear(models.Model): #Популярные навыки за разные года (ТОП-20)
    year = models.IntegerField() #Год
    name = models.CharField(max_length=255)  # Название навыка
    count = models.IntegerField()  # Количество упоминаний

    def __str__(self):
        return self.name

class SkillByYearSum(models.Model): #Популярные навыки за разные года (ТОП-20)
    year = models.IntegerField() #Год
    name = models.CharField(max_length=255)  # Название навыка
    count = models.IntegerField()  # Количество упоминаний

    def __str__(self):
        return self.name

#Востребованность

class VacancyStatistic(models.Model): #Количество вакансий по годам - общее
    year = models.CharField(max_length=4)
    vacancy_count = models.IntegerField()

    def __str__(self):
        return f"{self.year} - {self.vacancy_count} вакансий"

    class Meta:
        db_table = 'vacancy_statistic'
        verbose_name = "Кол-во вакансий"
        verbose_name_plural = "Кол-во вакансий"

class BackendVacancyStatistic(models.Model): #Количество вакансий по годам - Backend
    year = models.CharField(max_length=4)
    vacancy_count = models.IntegerField()

    def __str__(self):
        return f"{self.year} - {self.vacancy_count} вакансий"

    class Meta:
        db_table = 'backend_vacancy_statistic'
        verbose_name = "Кол-во вакансий Backend"
        verbose_name_plural = "Кол-во вакансий Backend"

class AverageSalary(models.Model): #Динамика уровня зарплат по годам - общее
    year = models.CharField(max_length=4)
    name = models.CharField(max_length=255)
    salary =  models.IntegerField(null=True, default=None)

    class Meta:
        db_table = 'average_salary'
        verbose_name = "Средняя зарплата"
        verbose_name_plural = "Средняя зарплата"

class BackendAverageSalary(models.Model): #Динамика уровня зарплат по годам - Backend
    year = models.CharField(max_length=4)
    name = models.CharField(max_length=255)
    salary =  models.IntegerField(null=True, default=None)

    class Meta:
        db_table = 'backend_average_salary'
        verbose_name = "Средняя зарплата Backend"
        verbose_name_plural = "Средняя зарплата Backend"

#География

class Salary(models.Model): #Уровень зарплат по городам для всех (порядок убывания)
    area_name = models.CharField(max_length=255)
    average_salary = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.average_salary}"

    class Meta:
        db_table = 'salary'
        verbose_name = "Уровень зарплат по городам"
        verbose_name_plural = "Уровень зарплат по городам"

class SalaryBackend(models.Model): #Уровень зарплат по городам для выбранной профессии (порядок убывания)
    area_name = models.CharField(max_length=255)
    average_salary = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.average_salary}"

    class Meta:
        db_table = 'salary_backend'
        verbose_name = "Уровень зарплат по городам по Backend"
        verbose_name_plural = "Уровень зарплат по городам по Backend"

class PartArea(models.Model): #Доля зарплат по городам для всех (порядок убывания)
    area_name = models.CharField(max_length=255)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.percentage}"

    class Meta:
        db_table = 'part_area'
        verbose_name = "Доля вакансий по городам"
        verbose_name_plural = "Доля вакансий по городам"

class PartAreaBackend(models.Model): #Доля зарплат по городам для Backend (порядок убывания)
    area_name = models.CharField(max_length=255)
    percentage = models.FloatField()

    def __str__(self):
        return f"{self.area_name} - {self.percentage}"

    class Meta:
        db_table = 'part_area_backend'
        verbose_name = "Доля вакансий по городам для Backend"
        verbose_name_plural = "Доля вакансий по городам для Backend"

#Графики

class GraphImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='graphs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DataTable(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(help_text="HTML содержимое для таблицы")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

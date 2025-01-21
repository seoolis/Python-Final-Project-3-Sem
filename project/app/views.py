import json
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SalaryBackend, PartAreaBackend, AverageSalary
from .models import BackendAverageSalary, BackendVacancyStatistic
from .models import SkillsBackend, SkillsBackendByYear
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import VacancyStatistic, BackendVacancyStatistic, Salary, PartArea, SkillByYear
from django.db.models import Count
#from django.contrib.auth.decorators import login_required

def index(request):
    data = {
        'title': 'Главная',
    }
    return render(request, 'main/index.html', data)

#@login_required
def general(request):
    # Получаем доступные года для фильтрации (сортируем по убыванию)
    years = SkillByYear.objects.values_list('year', flat=True).distinct().order_by('-year')

    # По умолчанию выбираем 2024 год
    selected_year = request.GET.get('year', '2024')

    # Данные для выбранного года (ТОП-20 навыков)
    top_skills_by_year = SkillByYear.objects.filter(year=selected_year).order_by('-count')[:20]

    # Данные для графиков (например, динамика зарплат и вакансий)
    salary_by_year = AverageSalary.objects.all().order_by('year')
    vacancies_by_year = VacancyStatistic.objects.all().order_by('year')
    city_salary_data = Salary.objects.all().order_by('-average_salary')
    city_vacancy_data = PartArea.objects.all().order_by('-percentage')

    # Преобразуем данные в формат JSON для использования в Chart.js
    salary_year_data = [{"year": row.year, "salary": row.salary} for row in salary_by_year]
    vacancy_year_data = [{"year": row.year, "vacancy_count": row.vacancy_count} for row in vacancies_by_year]
    city_salary = [{"city": row.area_name, "salary": row.average_salary} for row in city_salary_data]
    city_vacancy = [{"city": row.area_name, "percentage": row.percentage} for row in city_vacancy_data]
    top_skills = [{"year": row.year, "name": row.name, "count": row.count} for row in top_skills_by_year]

    # Передаем все данные в контексте для использования в шаблоне
    context = {
        'salary_by_year': salary_by_year,
        'vacancies_by_year': vacancies_by_year,
        'city_salary_data': city_salary_data,
        'city_vacancy_data': city_vacancy_data,
        'top_skills_by_year': top_skills_by_year,
        'selected_year': selected_year,
        'years': years,
        'salary_year_data': json.dumps(salary_year_data),
        'vacancy_year_data': json.dumps(vacancy_year_data),
        'city_salary': json.dumps(city_salary),
        'city_vacancy': json.dumps(city_vacancy),
        'top_skills': json.dumps(top_skills),
        'title': 'Общая статистика',
    }

    return render(request, 'main/general.html', context)

def demand(request):
    # Динамика уровня зарплат по годам
    salary_by_year = BackendAverageSalary.objects.all().order_by('year')

    # Динамика количества вакансий по годам
    vacancies_by_year = BackendVacancyStatistic.objects.all().order_by('year')

    # Преобразуем данные в формат JSON для использования в Chart.js
    salary_year_data = [{"year": row.year, "salary": row.salary} for row in salary_by_year]
    vacancy_year_data = [{"year": row.year, "vacancy_count": row.vacancy_count} for row in vacancies_by_year]

    context = {
        'salary_by_year': salary_by_year,
        'vacancies_by_year': vacancies_by_year,
        'salary_year_data': json.dumps(salary_year_data),
        'vacancy_year_data': json.dumps(vacancy_year_data),
        'title': 'Востребованность',
    }
    return render(request, 'main/demand.html', context)


def skills(request):
    # Определяем текущий год
    default_year = 2024

    # Получаем выбранный год из запроса или устанавливаем по умолчанию 2024
    selected_year = int(request.GET.get('year', default_year))

    # Фильтруем данные по выбранному году
    skills_data = SkillsBackendByYear.objects.filter(year=selected_year).order_by('-count')[:20]

    # Генерируем список годов (2015–2024)
    years = list(range(2015, 2025))

    # Преобразуем данные в формат JSON для использования в Chart.js
    skills_json_data = [{"name": skill.name, "count": skill.count} for skill in skills_data]

    context = {
        'skills_data': skills_data,
        'years': years,
        'selected_year': selected_year,
        'skills_json_data': json.dumps(skills_json_data),
        'title': 'Навыки',
    }
    return render(request, 'main/skills.html', context)


def geography(request):
    # Уровень зарплат по городам для Backend-разработчиков
    city_salary_data = SalaryBackend.objects.all().order_by('-average_salary')[:10]  # ТОП-10 по убыванию зарплат

    # Доля вакансий по городам для Backend-разработчиков
    city_vacancy_data = PartAreaBackend.objects.all().order_by('-percentage')[:10]  # ТОП-10 по убыванию доли

    # Преобразуем данные в формат JSON для использования в Chart.js
    city_salary = [{"city": row.area_name, "salary": row.average_salary} for row in city_salary_data]
    city_vacancy = [{"city": row.area_name, "percentage": row.percentage} for row in city_vacancy_data]

    context = {
        'city_salary_data': city_salary_data,
        'city_vacancy_data': city_vacancy_data,
        'city_salary': json.dumps(city_salary),
        'city_vacancy': json.dumps(city_vacancy),
        'title': 'География',
    }

    return render(request, 'main/geography.html', context)

def vacancies(request):
    return render(request, 'main/vacancies.html')

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Пользователь {user.username} успешно зарегистрирован.")  # Это поможет понять, что регистрация прошла
            messages.success(request, 'Вы успешно зарегистрировались!')
            login(request, user)  # Авторизация сразу после регистрации
            return redirect('home')  # Перенаправление на главную страницу
        else:
            print("Форма не прошла валидацию.")  # Это покажет, если форма невалидна
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль!')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logoutPage(request):
    logout(request)
    return redirect('login')
from datetime import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import SalaryBackend, PartAreaBackend
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
    # Динамика уровня зарплат по годам
    salary_by_year = BackendAverageSalary.objects.all().order_by('year')

    # Динамика количества вакансий по годам
    vacancies_by_year = VacancyStatistic.objects.all().order_by('year')

    # Уровень зарплат по городам для всех профессий
    city_salary_data = Salary.objects.all().order_by('-average_salary')

    # Доля вакансий по городам для всех профессий
    city_vacancy_data = PartArea.objects.all().order_by('-percentage')

    # ТОП-20 навыков по годам (оставляем только шаблон)

    context = {
        'salary_by_year': salary_by_year,
        'vacancies_by_year': vacancies_by_year,
        'city_salary_data': city_salary_data,
        'city_vacancy_data': city_vacancy_data,
        'title': 'Общая статистика',
    }

    return render(request, 'main/general.html', context)

def demand(request):
    # Динамика уровня зарплат по годам
    salary_by_year = BackendAverageSalary.objects.all().order_by('year')

    # Динамика количества вакансий по годам
    vacancies_by_year = BackendVacancyStatistic.objects.all().order_by('year')

    context = {
        'salary_by_year': salary_by_year,
        'vacancies_by_year': vacancies_by_year,
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

    context = {
        'skills_data': skills_data,
        'years': years,
        'selected_year': selected_year,
        'title': 'Навыки',
    }
    return render(request, 'main/skills.html', context)

def geography(request):
    # Уровень зарплат по городам для Backend-разработчиков
    city_salary_data = SalaryBackend.objects.all().order_by('-average_salary')[:10]  # ТОП-10 по убыванию зарплат

    # Доля вакансий по городам для Backend-разработчиков
    city_vacancy_data = PartAreaBackend.objects.all().order_by('-percentage')[:10]  # ТОП-10 по убыванию доли

    context = {
        'city_salary_data': city_salary_data,
        'city_vacancy_data': city_vacancy_data,
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
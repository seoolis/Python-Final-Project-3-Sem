from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def index(request):
    data = {
        'title': 'Главная',
    }
    return render(request, 'main/index.html', data)

@login_required
def general(request):
    return render(request, 'main/general.html')

def demand(request):
    return render(request, 'main/demand.html')

def skills(request):
    return render(request, 'main/skills.html')

def geography(request):
    return render(request, 'main/geography.html')

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
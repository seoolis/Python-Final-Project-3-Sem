from django.shortcuts import render

def index(request):
    data = {
        'title': 'Главная',
    }
    return render(request, 'main/index.html', data)

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
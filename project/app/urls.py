from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home'),
    path('general', views.general, name = 'statistic'),
    path('demand', views.demand, name = 'demand'),
    path('skills', views.skills, name = 'skills'),
    path('geography', views.geography, name = 'geography'),
    path('vacancies', views.vacancies, name = 'vacancies'),
    path('login', views.loginPage, name = 'login'),
    path('register', views.registerPage, name = 'register'),
    path('logout', views.logoutPage, name='logout'),
]

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#Создаение урл адресов частных приложений

urlpatterns = [
    # Предыдущая версия
    #path('login/', views.user_login, name = 'login'),

    #Новая версия url-адреса для входа и выхода
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name  = 'logout'),

    #Путь к dashboard
    path('', views.dashboard, name = 'dashboard'),
]
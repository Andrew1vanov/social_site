from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth.decorators import login_required

# Create your views here.

##Добавление встроенного фреймворка аутентификации
@login_required #проверяет аутентификацию текущего пользователя
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

##Создание собственной функции аутентификации
def user_login(request):
    if request.method == 'POST': #при нажатии входа 
        form = LoginForm(request.POST)#создается экземпляр формы
        if form.is_valid():#если форма верна (поля заполнены верно)
            cd = form.cleaned_data
            user = authenticate(request, 
                                username = cd['user_name'],#Из-за моего названия переменной есть отличие от книги
                                password = cd['password'])
            if user is not None: #Если пользователь существует
                if user.is_active:#Если пользоваетль активен (не отклчена учетная запись)
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled acoount')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


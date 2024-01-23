from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit = False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект user
            new_user.save()
            Profile.objects.create(user = new_user)
            return render(request, 'account/template/register_done.html', 
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/template/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance = request.user, data = request.POST)
        profile_form = ProfileEditForm(instance = request.user.profile, data = request.POST,
                                       files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfuly')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance = request.user)
        profile_form = ProfileEditForm(instance= request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 
                                                 'profile_form': profile_form})

import logging

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from users.forms import UserRegisterForm, LoginForm
from users.models import Profile


def user_login(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('main:index')
            else:
                return render(
                    request,
                    'users/login.html', {'form': form, 'error': 'Неверный логин или пароль'}
                )
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form, 'error': ''})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('main:index')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            Profile.objects.create(
                user=form.instance,
                middle_name=form.cleaned_data["middle_name"],
                phone='7' + ''.join(c for c in form.cleaned_data["phone"] if c.isdigit())
            )
            return redirect('users:login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')


@require_POST
def check_user(request):
    column_name = request.POST.get('column_name', None)
    column_value = request.POST.get('column_value', None)
    if column_name is None or column_value is None:
        raise BadRequest('Invalid request data')

    try:
        if column_name == 'phone':
            print(column_value)
            return JsonResponse({'is_taken': Profile.objects.filter(phone=column_value).exists()})
        else:
            return JsonResponse({'is_taken': User.objects.filter(**{column_name: column_value}).exists()})
    except Exception as e:
        logging.warning(e, exc_info=True)
        raise BadRequest('Invalid request data')

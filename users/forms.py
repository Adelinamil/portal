import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


def validate_names(value):
    if not re.match(r'^[а-яА-Я\-]+$', value):
        raise forms.ValidationError('Только кириллица, пробел и тире разрешены')
    return value


def validate_phone(value):
    if not re.match(r'^\(\d{3}\)-\d{3}-\d{2}-\d{2}$', value):
        raise forms.ValidationError('Номер телефона не соответствует формату')
    if Profile.objects.filter(phone='7' + ''.join(c for c in value if c.isdigit())).exists():
        raise forms.ValidationError('Этот номер телефона уже занят')

    return value


def validate_username(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise forms.ValidationError('Только латиница, цифры и тире разрешены')
    if User.objects.filter(username=value).exists():
        raise forms.ValidationError('Это имя пользователя уже занято')
    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError('Эта почта уже занята')
    return value


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Почта',
        validators=[validate_email],
        widget=forms.EmailInput(
            attrs={
                'placeholder': '2bJtT@example.com',
                'oninput': 'validateEmail()'
            }
        )
    )
    phone = forms.CharField(
        label='Номер телефона',
        max_length=15,
        validators=[validate_phone],
        widget=forms.TextInput(
            attrs={
                'placeholder': '(777)-777-77-77', 'pattern': r'^\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
                'type': 'tel',
                'aria-describedby': 'phonePlus',
                'oninput': 'validatePhone()'
            }
        )
    )
    last_name = forms.CharField(
        max_length=100,
        label='Фамилия',
        validators=[validate_names],
        widget=forms.TextInput(
            attrs={
                'pattern': '[а-яА-Я\\-]+',
                'placeholder': 'Иванов'
            }
        ),
    )
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        validators=[validate_names],
        widget=forms.TextInput(
            attrs={
                'pattern': '[а-яА-Я\\-]+',
                'placeholder': 'Иван'
            }
        ),
    )
    middle_name = forms.CharField(
        max_length=100,
        label='Отчество',
        validators=[validate_names],
        widget=forms.TextInput(
            attrs={
                'pattern': '[а-яА-Я\\-]+',
                'placeholder': 'Иванович'
            }
        ),
    )
    username = forms.CharField(
        max_length=30,
        label='Имя пользователя',
        help_text='Разрешены только латиница, цифры и _',
        validators=[validate_username],
        widget=forms.TextInput(
            attrs={
                'pattern': '[a-zA-Z0-9_]+',
                'oninput': 'validateUsername()',
                'placeholder': 'ivan2033'
            }
        ),
    )
    confirm = forms.BooleanField(label='Согласие на обработку данных', required=True)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise forms.ValidationError('Только латиница, цифры и тире разрешены')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Это имя пользователя уже занято')
        return username

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'last_name', 'first_name', 'middle_name', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

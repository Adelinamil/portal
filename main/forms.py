import re

from django import forms
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.forms import HiddenInput

from .models import Violation


def validate_vehicle_number(value):
    if not re.match(
            r'^(([АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{1,2})(\d{2,3})|(\d{4}[АВЕКМНОРСТУХ]{2})'
            r'(\d{2})|(\d{3}C?D{1,2}\d{3})(\d{2})|([АВЕКМНОРСТУХ]{2}\d{3}[АВЕКМНОРСТУХ])(\d{2})|'
            r'([АВЕКМНОРСТУХ]\d{4})(\d{2})|(\d{3}[АВЕКМНОРСТУХ])(\d{2})|(\d{4}[АВЕКМНОРСТУХ])(\d{2}))$',
            value
    ):
        raise forms.ValidationError('Только латиница, цифры и тире разрешены')
    return value


class ViolationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=HiddenInput())
    vehicle_number = forms.CharField(
        label='Регистрационный номер автомобиля',
        max_length=10,
        widget=forms.TextInput(
            attrs={
                'title': 'Введите корректный номер автомобиля'
            }
        )
    )
    description = forms.CharField(
        label='Описание нарушения',
        min_length=10,
        max_length=2000,
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})
    )
    proof = forms.FileField(
        label='Доказательства',
        widget=forms.FileInput(attrs={'accept': 'image/*,video/*,.doc,.docx,.pdf'}),
        validators=[
            FileExtensionValidator(
                ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'doc', 'docx', 'pdf'],
                'Недопустимый формат файла'
            )
        ],
        required=False
    )

    class Meta:
        model = Violation
        fields = ['user', 'vehicle_number', 'description', 'proof']

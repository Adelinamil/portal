from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):  # Расширение модели User через Proxy Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Дополнительная информация'

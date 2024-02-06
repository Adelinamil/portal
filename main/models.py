from django.contrib.auth.models import User
from django.db import models


class Violation(models.Model):
    NEW = 'NEW'
    CONFIRMED = 'CONFIRMED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = {
        NEW: 'Новое',
        CONFIRMED: 'Подтверждено',
        REJECTED: 'Отклонено',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='violations')
    vehicle_number = models.CharField(max_length=10, verbose_name='Регистрационный номер автомобиля')
    description = models.TextField(verbose_name='Описание нарушения')
    proof = models.FileField(upload_to='proofs/%Y/%m/%d/', verbose_name='Доказательства', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=tuple(STATUS_CHOICES.items()),
        default=NEW,
        verbose_name='Статус'
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    @property
    def short_description(self):
        return self.description if len(self.description) < 35 else (self.description[:33] + '...')

    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'

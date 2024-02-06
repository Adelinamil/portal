from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Дополнительная информация"


class UserAdmin(BaseUserAdmin):  # для отображения дополнительных полей пользователя в админке
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

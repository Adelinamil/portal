from django.contrib import admin
from django.utils.html import format_html

from .models import Violation

admin.site.site_header = 'Нарушениям.Нет'


@admin.register(Violation)
class ViolationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'full_name', 'vehicle_number', 'show_description', 'status')
    sortable_by = ('id', 'created', 'full_name', 'vehicle_number', 'status')
    list_filter = ('status',)
    search_fields = (
        'user__last_name', 'user__first_name', 'user__profile__middle_name', 'vehicle_number', 'description'
    )
    search_help_text = 'Поиск по ФИО, регистрационному номеру автомобиля, описанию'
    list_editable = ('status',)
    ordering = ('created',)

    def full_name(self, obj):
        if getattr(obj.user, 'profile', None):
            return f"{obj.user.last_name} {obj.user.first_name} {obj.user.profile.middle_name}"
        return f"{obj.user.last_name} {obj.user.first_name}"

    full_name.short_description = 'ФИО'

    @admin.display(description="Описание")
    def show_description(self, obj):
        return format_html(
            '<span style="text-overflow: ellipsis; cursor: help" title="{}">{}</span>',
            obj.description,
            obj.short_description
        )

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        return ['id', 'user', 'vehicle_number', 'description', 'proof', 'created', 'updated']

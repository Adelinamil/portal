from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('violations/', views.get_violations, name='violations'),
    path('violations/create/', views.create_violation, name='create_violation'),
    path('violation/<int:violation_id>/', views.get_violation, name='violation'),
]

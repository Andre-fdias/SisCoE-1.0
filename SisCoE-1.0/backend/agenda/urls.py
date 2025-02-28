# backend/agenda/urls.py

from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('calendario/', views.calendario, name='calendario'),
    path('lembrete/novo/', views.lembrete_novo, name='lembrete_novo'),
    path('lembrete/editar/<int:pk>/', views.lembrete_editar, name='lembrete_editar'),
    path('lembrete/deletar/<int:pk>/', views.lembrete_deletar, name='lembrete_deletar'),
    path('tarefa/novo/', views.tarefa_nova, name='tarefa_nova'),
    path('tarefa/editar/<int:pk>/', views.tarefa_editar, name='tarefa_editar'),
    path('tarefa/deletar/<int:pk>/', views.tarefa_deletar, name='tarefa_deletar'),



]
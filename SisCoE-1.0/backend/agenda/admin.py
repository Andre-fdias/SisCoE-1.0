from django.contrib import admin
from .models import Lembrete, Tarefa

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data', 'tipo', 'cor')
    search_fields = ('titulo', 'descricao')
    list_filter = ('data', 'tipo')

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'descricao', 'data_inicio', 'data_fim', 'tipo', 'cor')
    search_fields = ('titulo', 'descricao')
    list_filter = ('data_inicio', 'data_fim', 'tipo')
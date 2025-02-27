from django import forms
from .models import Lembrete, Tarefa

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ['titulo', 'descricao', 'data', 'cor', 'visibilidade']

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'data_inicio', 'data_fim', 'cor', 'visibilidade']
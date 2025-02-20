from django import forms
from .models import Pessoal, Contato, Posto, Cidade

class PessoalForm(forms.ModelForm):
    class Meta:
        model = Pessoal
        fields = '__all__'
        widgets = {
            'posto': forms.HiddenInput()
        }

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = '__all__'
        widgets = {
            'posto': forms.HiddenInput()
        }

class PostoForm(forms.ModelForm):
    class Meta:
        model = Posto
        fields = '__all__'

class CidadeForm(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = '__all__'
        widgets = {
            'posto': forms.HiddenInput()
        }
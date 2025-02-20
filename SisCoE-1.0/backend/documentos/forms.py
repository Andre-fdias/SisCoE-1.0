from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = '__all__'
        widgets = {
            'data_publicacao': forms.DateInput(attrs={'type': 'date'}),
            'data_documento': forms.DateInput(attrs={'type': 'date'}),
        }
from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    data_publicacao = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Documento
        fields = ['data_publicacao', 'assunto', 'numero_documento', 'tipo', 'descricao', 'assinada_por']
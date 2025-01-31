# accounts/forms.py
from django import forms

from django.utils.translation import gettext_lazy as _

from backend.accounts.models import User


class CustomUserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nome Completo',
        max_length=150,
    )
    last_name = forms.CharField(
        label='Nome de Guerra',
        max_length=150,
    )
    email = forms.EmailField(
        label='E-mail Funcional',
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )
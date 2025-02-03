# core/admin.py
from django.contrib import admin
from .models import Profile  # Certifique-se de importar o modelo Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'posto_grad', 'cpf', 'tipo')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'cpf')
    list_filter = ('posto_grad', 'tipo')

# Registrar o modelo Profile no admin do app core
admin.site.register(Profile, ProfileAdmin)
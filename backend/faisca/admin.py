from django.contrib import admin
from .models import Chat


# registra os modelos de dados(models.py) no admin/django .
admin.site.register(Chat)

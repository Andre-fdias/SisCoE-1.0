from django.contrib import admin
from .models import Chat, Conversation


# registra os modelos de dados(models.py) no admin/django .
admin.site.register(Chat)
admin.site.register(Conversation)

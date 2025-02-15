# models.py
from django.db import models
from backend.accounts.models import User
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    arquivado = models.BooleanField(default=False)

    def __str__(self):
        return self.message
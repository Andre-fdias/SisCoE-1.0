from django.db import models
from backend.accounts.models import User


class Chat(models.Model):
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)  # 
    arquivado = models.BooleanField(default=False)
    
    def __str__(self):
      return self.message 
from django.urls import path
from . import views

app_name = 'faisca'

urlpatterns = [
    path('chat', views.chatbot, name='chatbot'),
    path('history', views.chat_history, name='chat_history'),
    path('reset_chat', views.reset_chat, name='reset_chat'),  # Adicione esta linha
]
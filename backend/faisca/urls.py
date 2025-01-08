from django.urls import path
from . import views

app_name = 'faisca'

urlpatterns = [
    path('chat', views.chatbot, name='chatbot'),
    path('reset_chat', views.reset_chat, name='reset_chat'),  # Rota para resetar o chat
    path('reset_and_redirect', views.reset_and_redirect, name='reset_and_redirect'),  # Nova rota para resetar e redirecionar
]
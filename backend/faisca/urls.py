from django.urls import path
from . import views

app_name = 'faisca'


urlpatterns = [
    path('chat', views.chatbot, name='chatbot'),
    path('history', views.chat_history, name='chat_history'),
]
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('home', views.index, name='index'),
    path('', views.capa, name='capa'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
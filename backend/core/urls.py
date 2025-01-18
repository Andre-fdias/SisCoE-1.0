from django.urls import path

from backend.core import views as v

app_name = 'core'


urlpatterns = [
    path('home', v.index, name='index'),  # noqa E501
    path('', v.capa, name='capa'),  # noqa E501
    path('profile/', v.profile, name='profile'),  # Adicione a URL para a página de perfil
    path('dashboard/', v.dashboard, name='dashboard'),
]
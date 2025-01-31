from django.urls import path

from backend.core import views as v

app_name = 'core'


urlpatterns = [
    path('home', v.index, name='index'),  # noqa E501
    path('', v.capa, name='capa'),  # noqa E501
    path('dashboard/', v.dashboard, name='dashboard'),
    path('profiles/', v.profile_list, name='profile_list'),
    path('profiles/<int:pk>/', v.profile_detail, name='profile_detail'),
    path('profiles/create/', v.profile_create, name='profile_create'),
    path('profiles/<int:pk>/update/', v.profile_update, name='profile_update'),
    path('profiles/<int:pk>/delete/', v.profile_delete, name='profile_delete'),
]
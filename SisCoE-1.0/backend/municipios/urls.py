from django.urls import path
from . import views as v

app_name = 'municipios'

urlpatterns = [
    path('', v.posto_list, name='posto_list'),
    path('<int:pk>/', v.posto_detail, name='posto_detail'),
    path('municipio/<int:pk>/', v.municipio_detail, name='municipio_detail'),  # Nova linha
    path('novo/', v.posto_create, name='posto_create'),
    path('<int:pk>/editar/', v.posto_update, name='posto_update'),
    path('<int:pk>/deletar/', v.posto_delete, name='posto_delete'),
]
from django.urls import path
from . import views

app_name = 'adicional'

urlpatterns = [
    path('cadastrar_lp/', views.cadastrar_lp, name="cadastrar_lp"),
    path('listar_lp/', views.listar_lp, name="listar_lp"),
    path('ver_lp/<int:id>/', views.ver_lp, name="ver_lp"),
    path('editar_lp/<int:id>/', views.editar_lp, name='editar_lp'),
    path('excluir_lp/<int:id>/', views.excluir_lp, name='excluir_lp'),
    path('historico_lp/<int:id>/', views.historico_lp, name='historico_lp'),
    path('buscar_militar_adicional/', views.buscar_militar2, name='buscar_militar_adicional'),
]
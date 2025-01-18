from django.urls import path
from . import views

app_name = 'adicional'

urlpatterns = [
    path('cadastrar_rpt/', views.cadastrar_rpt, name="cadastrar_rpt"),
    path('listar_rpt/', views.listar_rpt, name="listar_rpt"),
    path('ver_rpt/<int:id>/', views.ver_rpt, name="ver_rpt"),
    path('rpt/editar_rpt/<int:id>/',views.editar_rpt, name='editar_rpt'),
    path('excluir_rpt/<int:id>/', views.excluir_rpt, name='excluir_rpt'),
    path('search_cadastro/', views.search_cadastro, name='search_cadastro'),
    path('buscar_militar_rpt/', views.buscar_militar_rpt, name='buscar_militar_rpt'),
    path('historico_rpt/<int:id>/', views.historico_rpt, name='historico_rpt'),
]



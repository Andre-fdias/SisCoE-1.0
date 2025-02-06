# bookstore/urls.py
from django.urls import path
from . import views

app_name = 'efetivo'

urlpatterns = [
    path('cadastrar_militar/', views.cadastrar_militar, name="cadastrar_militar"),
    path('listar_militar/', views.listar_militar, name="listar_militar"),
    path('ver_militar/<int:id>/', views.ver_militar, name="ver_militar"),
    path('editar_posto_graduacao/<int:id>/', views.editar_posto_graduacao, name='editar_posto_graduacao'),
    path('editar_situacao_funcional/<int:id>/', views.editar_situacao_funcional, name='editar_situacao_funcional'),
    path('editar_dados_pessoais_contatos/<int:id>/', views.editar_dados_pessoais_contatos, name='editar_dados_pessoais_contatos'),
    path('excluir_militar/<int:id>/', views.excluir_militar, name='excluir_militar'),
    path('editar_imagem/<int:id>/', views.editar_imagem, name='editar_imagem'),
    path('historico_movimentacoes/<int:id>/', views.historico_movimentacoes, name='historico_movimentacoes'),
    path('editar_situacao_atual/<int:id>/', views.editar_situacao_atual, name='editar_situacao_atual'),
    path('cadastrar_nova_situacao/<int:id>/', views.cadastrar_nova_situacao, name='cadastrar_nova_situacao'),
    path('check_rpt/<int:id>/', views.check_rpt, name='check_rpt'),
]

from django.urls import path
from . import views


app_name = 'documentos'

urlpatterns = [
    path('', views.listar_documentos, name='listar_documentos'),
    path('documento/<int:pk>/', views.detalhe_documento, name='detalhe_documento'),
    path('criar/', views.criar_documento, name='criar_documento'),
    path('editar/<int:pk>/', views.editar_documento, name='editar_documento'),
    path('excluir/<int:pk>/', views.excluir_documento, name='excluir_documento'),
    path('carrossel/', views.carrossel_noticias, name='carrossel_noticias'),
    path('conteudo/<int:pk>/', views.carregar_conteudo_arquivo, name='carregar_conteudo_arquivo'),
    # ...
    path('documento/editar/<int:pk>/', views.editar_documento, name='editar_documento'),
    path('arquivo/remover/<int:pk>/', views.remover_arquivo, name='remover_arquivo'),
  

]
from django.urls import path
from . import views

app_name = 'bm'

urlpatterns = [
    path('cadastrar_bm/', views.cadastrar_bm, name="cadastrar_bm"),
    path('listar_bm/', views.listar_bm, name="listar_bm"),
    path('editar_bm/<int:id>/', views.editar_bm, name="editar_bm"),
    path('ver_bm/<int:pk>/', views.ver_bm, name="ver_bm"),  # Use 'pk' aqui
    path('excluir_bm/<int:id>/', views.excluir_bm, name='excluir_bm'),
 
]
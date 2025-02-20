# admin.py
from django.contrib import admin
from .models import Documento, Arquivo

class ArquivoInline(admin.TabularInline):
    model = Arquivo
    extra = 1

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    inlines = [ArquivoInline]
    list_display = ('assunto', 'tipo', 'data_publicacao', 'usuario')
    list_filter = ('tipo', 'data_publicacao', 'usuario')
    search_fields = ('assunto', 'numero_documento')
    date_hierarchy = 'data_publicacao'

@admin.register(Arquivo)
class ArquivoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'tipo', 'arquivo')
    list_filter = ('tipo',)
    search_fields = ('documento__assunto',)
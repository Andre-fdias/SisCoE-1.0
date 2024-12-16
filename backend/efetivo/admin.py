from django.contrib import admin

from .models import (
    Cadastro,
    DetalhesSituacao,
    HistoricoDetalhesSituacao,
    HistoricoPromocao,
    Imagem,
    Promocao
)


@admin.register(Cadastro)
class CadastroAdmin(admin.ModelAdmin):
    list_display = ('nome','re','dig','email',)
    search_fields = ('re', 'nome')
    list_filter = ('re',)


@admin.register(Promocao)
class PromocaoAdmin(admin.ModelAdmin):
    list_display = ('__str__','posto_grad','quadro','grupo',)
    search_fields = ('cadastro__re',
                     'cadastro__nome')
    list_filter = ('posto_grad',)


@admin.register(Imagem)
class ImagemAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('promocao__posto_grad',
                     'cadastro__re',
                     'cadastro__nome')
    list_filter = ('image',)


@admin.register(DetalhesSituacao)
class DetalhesSituacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__','situacao','sgb','posto_secao','cat_efetivo','op_adm',)
    search_fields = ('cadastro__re',
                     'cadastro__nome')
    list_filter = ('situacao',)


@admin.register(HistoricoDetalhesSituacao)
class HistoricoDetalhesSituacaoAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'situacao')
    search_fields = ('cadastro__re',
                     'cadastro__nome')
    list_filter = ('situacao',)
    date_hierarchy = 'data_alteracao'


@admin.register(HistoricoPromocao)
class HistoricoPromocaoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'posto_grad')
    search_fields = ('cadastro__re',
                     'cadastro__nome')
    list_filter = ('posto_grad',)
    date_hierarchy = 'data_alteracao'

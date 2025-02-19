from django.contrib import admin
from django.utils.html import format_html
from .models import Posto, Cidade, Contato, Pessoal

class ContatoInline(admin.TabularInline):
    model = Contato
    extra = 1
    classes = ('collapse',)
    fields = ('telefone', 'email', 'cep', 'cidade')

class PessoalInline(admin.TabularInline):
    model = Pessoal
    extra = 1
    classes = ('collapse',)
    fieldsets = (
        (None, {
            'fields': ('cel', 'ten_cel', 'maj', 'cap', 'tenqo', 'tenqa', 'asp', 'st_sgt', 'cb_sd')
        }),
    )

class CidadeInline(admin.StackedInline):
    model = Cidade
    extra = 1
    fields = ('municipio', 'bandeira', 'latitude', 'longitude')
    readonly_fields = ('bandeira_preview',)
    
    def bandeira_preview(self, instance):
        if instance.bandeira:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                instance.bandeira.url
            )
        return "Sem imagem"
    bandeira_preview.short_description = "Pré-visualização"

@admin.register(Posto)
class PostoAdmin(admin.ModelAdmin):

    readonly_fields = ('quartel_preview',)
    
    def quartel_preview(self, obj):
        if obj.quartel:
            return format_html(
                '<img src="{}" style="max-height: 200px;"/>',
                obj.quartel.url
            )
        return "Nenhuma imagem cadastrada"
    quartel_preview.short_description = "Pré-visualização do Quartel"

    fieldsets = (
        ('Identificação', {
            'fields': ('sgb', 'posto_secao', 'posto_atendimento', 'quartel', 'quartel_preview')
        }),
        ('Localização', {
            'fields': ('cidade_posto', 'tipo_cidade', 'op_adm')
        }),
        ('Registro', {
            'classes': ('collapse',),
            'fields': ('usuario', 'data_criacao'),
        }),
    )

    inlines = [CidadeInline, ContatoInline, PessoalInline]
    list_display = ('posto_atendimento', 'sgb_display', 'cidade_posto', 'tipo_cidade')
    search_fields = ('posto_atendimento', 'cidade_posto')
    list_filter = ('sgb', 'op_adm')
    ordering = ('-data_criacao',)
    
    def sgb_display(self, obj):
        return obj.get_sgb_display()
    sgb_display.short_description = 'SGB'

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'posto_link', 'bandeira_preview')
    search_fields = ('municipio', 'posto__posto_atendimento')
    list_select_related = ('posto',)
    
    def posto_link(self, obj):
        return format_html(
            '<a href="/admin/municipios/posto/{}/change/">{}</a>',
            obj.posto.id,
            obj.posto.posto_atendimento
        )
    posto_link.short_description = 'Posto'
    
    def bandeira_preview(self, obj):
        if obj.bandeira:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.bandeira.url
            )
        return "N/A"
    bandeira_preview.short_description = 'Bandeira'

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ('posto', 'telefone', 'email', 'cep')
    search_fields = ('posto__posto_atendimento', 'telefone', 'email')

@admin.register(Pessoal)
class PessoalAdmin(admin.ModelAdmin):
    list_display = ('posto', 'total_efetivo')
    search_fields = ('posto__posto_atendimento',)
    
    def total_efetivo(self, obj):
        return sum([
            obj.cel, obj.ten_cel, obj.maj, obj.cap,
            obj.tenqo, obj.tenqa, obj.asp, obj.st_sgt, obj.cb_sd
        ])
    total_efetivo.short_description = 'Total de Militares'

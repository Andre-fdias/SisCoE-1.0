from django.contrib import admin
from .models import Cadastro, DetalhesSituacao, Promocao, HistoricoDetalhesSituacao,HistoricoPromocao, Imagem


# registra os modelos de dados(models.py) no admin/django .
admin.site.register(Cadastro)
admin.site.register(DetalhesSituacao)
admin.site.register(Promocao)
admin.site.register(HistoricoDetalhesSituacao)
admin.site.register(HistoricoPromocao)
admin.site.register(Imagem)

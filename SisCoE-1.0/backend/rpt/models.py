from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from backend.efetivo.models import Cadastro

User = get_user_model()

class Cadastro_rpt(models.Model):


    status_choices = (
        ("", ""),
        ("Aguardando", "Aguardando"),
        ("Mov. serviço", "Mov. serviço"),
        ("Mov. própria", "Mov. própria"),
        ("Exclusão a pedido", "Exclusão a pedido"),
        ("Tranferido de Unidade", "Tranferido de Unidade"),
        ("Excluído Alt. quadro", "Excluído Alt. quadro"),
    )

    alteracao_choices = (
        ("", ""),
        ("Destino", "Destino"),
        ("Correção", "Correção"),
        ("Outros", "Outros"),
       
    )
    sgb_choices=( 
        ("", " "),                                                
        ("EM"," EM"),
        ("1ºSGB", "1ºSGB"),
        ("2ºSGB", "2ºSGB"),
        ("3ºSGB", "3ºSGB"),
        ("4ºSGB", "4ºSGB"),
        ("5ºSGB", "5ºSGB")
    )
    posto_secao_choices = (
         ("", " "),
         ("703150000 - CMT", "CMT"),
         ("703159000 - SUB CMT", "SUB CMT"),
         ("703159100 - SEC ADM", "SEC ADM"),
         ("703159110 - B/1 E B/5", "B/1 E B/5"),
         ("703159110-1 - B/5", "B/5"),
         ("703159120 - AA", "AA"),
         ("703159130 - B/3 E MOTOMEC", "B/3 E MOTOMEC"),
         ("703159130-1 - MOTOMEC", "MOTOMEC"),
         ("703159131 - COBOM", "COBOM"),
         ("703159140 - B/4", "B/4"),
         ("703159150 - ST UGE", "ST UGE"),
         ("703159160 - ST PJMD", "ST PJMD"),
         ("703159200 - SEC ATIV TEC", "SEC ATIV TEC"),
         ("703151000 - CMT 1º SGB", "CMT 1º SGB"),
         ("703151100 - ADM PB CERRADO", "ADM PB CERRADO"),
         ("703151101 - EB CERRADO", "EB CERRADO"),
         ("703151102 - EB ZONA NORTE", "EB ZONA NORTE"),
         ("703151200 - ADM PB SANTA ROSÁLIA", "ADM PB SANTA ROSÁLIA"),
         ("703151201 - EB SANTA ROSÁLIA", "EB SANTA ROSÁLIA"),
         ("703151202 - EB ÉDEM", "EB ÉDEM"),
         ("703151300 - ADM PB VOTORANTIM", "ADM PB VOTORANTIM"),
         ("703151301 - EB VOTORANTIM", "EB VOTORANTIM"),
         ("703151302 - EB PIEDADE", "EB PIEDADE"),
         ("703151800 - ADM 1º SGB", "ADM 1º SGB"),
         ("703152000 - CMT 2º SGB", "CMT 2º SGB"),
         ("703152100 - ADM PB ITU", "ADM PB ITU"),
         ("703152101 - EB ITU", "EB ITU"),
         ("703152102 - EB PORTO FELIZ", "EB PORTO FELIZ"),
         ("703152200 - ADM PB SALTO", "ADM PB SALTO"),
         ("703152201 - EB SALTO", "EB SALTO"),
         ("703152300 - ADM PB SÃO ROQUE", "ADM PB SÃO ROQUE"),
         ("703152301 - EB SÃO ROQUE", "EB SÃO ROQUE"),
         ("703152302 - EB IBIÚNA", "EB IBIÚNA"),
         ("703152800 - ADM 2º SGB", "ADM 2º SGB"),
         ("703152900 - NUCL ATIV TEC 2º SGB", "NUCL ATIV TEC 2º SGB"),
         ("703153000 - CMT 3º SGB", "CMT 3º SGB"),
         ("703153100 - ADM PB ITAPEVA", "ADM PB ITAPEVA"),
         ("703153101 - EB ITAPEVA", "EB ITAPEVA"),
         ("703153102 - EB APIAÍ", "EB APIAÍ"),
         ("703153103 - EB ITARARÉ", "EB ITARARÉ"),
         ("703153104 - EB CAPÃO BONITO", "EB CAPÃO BONITO"),
         ("703153800 - ADM 3º SGB", "ADM 3º SGB"),
         ("703153900 - NUCL ATIV TEC 3º SGB", "NUCL ATIV TEC 3º SGB"),
         ("703154000 - CMT 4º SGB", "CMT 4º SGB"),
         ("703154100 - ADM PB ITAPETININGA", "ADM PB ITAPETININGA"),
         ("703154101 - EB ITAPETININGA", "EB ITAPETININGA"),
         ("703154102 - EB BOITUVA", "EB BOITUVA"),
         ("703154103 - EB ANGATUBA", "EB ANGATUBA"),
         ("703154200 - ADM PB TATUÍ", "ADM PB TATUÍ"),
         ("703154201 - EB TATUÍ", "EB TATUÍ"),
         ("703154202 - EB TIETÊ", "EB TIETÊ"),
         ("703154203 - EB LARANJAL PAULISTA", "EB LARANJAL PAULISTA"),
         ("703154800 - ADM 4º SGB", "ADM 4º SGB"),
         ("703154900 - NUCL ATIV TEC 4º SGB", "NUCL ATIV TEC 4º SGB"),
         ("703155000 - CMT 5º SGB", "CMT 5º SGB"),
         ("703155100 - ADM PB BOTUCATU", "ADM PB BOTUCATU"),
         ("703155101 - EB BOTUCATU", "EB BOTUCATU"),
         ("703155102 - EB ITATINGA", "EB ITATINGA"),
         ("703155200 - ADM PB AVARÉ", "ADM PB AVARÉ"),
         ("703155201 - EB AVARÉ", "EB AVARÉ"),
         ("703155202 - EB PIRAJU", "EB PIRAJU"),
         ("703155203 - EB ITAÍ", "EB ITAÍ"),
         ("703155800 - ADM 5º SGB", "ADM 5º SGB"),
         ("703155900 - NUCL ATIV TEC 5º SGB", "NUCL ATIV TEC 5º SGB"),
      )
    

    id = models.AutoField(primary_key=True)
    data_pedido = models.DateField(blank=False, null=False)
    data_movimentacao = models.DateField(blank=True, null=True)  # Opcional
    data_alteracao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=status_choices)
    sgb_destino = models.CharField(max_length=50, choices=sgb_choices)
    posto_secao_destino = models.CharField(max_length=50, choices=posto_secao_choices)
    doc_solicitacao = models.CharField(max_length=50)
    doc_alteracao = models.CharField(max_length=50, blank=True, null=True)  # Opcional
    doc_movimentacao = models.CharField(max_length=50, blank=True, null=True)  # Opcional
    alteracao = models.CharField(max_length=50, choices=alteracao_choices, blank=True, null=True)  # Opcional
    cadastro = models.ForeignKey(Cadastro, related_name='cadastro_rpt', on_delete=models.DO_NOTHING)
    usuario_alteracao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.cadastro.re} {self.cadastro.dig} {self.cadastro.nome_de_guerra}'


    @property
    def ultima_imagem(self):
        return self.cadastro.imagens.last()

    @property
    def tempo_pedido_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.data_pedido)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def pedido_dias(self):
        hoje = datetime.today().date()
        delta = hoje -self.data_pedido
        return delta.days

    @property
    def pedido_status(self):
        dias = self.pedido_dias()
        if dias < 30:
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">- de 1 mês</span>')
        if dias < 180:
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">- de 06 meses</span>')
        if dias < 365:
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">- de 1 ano</span>')
        if dias < 730:
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">- de 2 anos</span>')
        if dias > 730:
            return mark_safe('<span class="bg-gray-800 text-white px-2 py-1 rounded">+ de 2 anos</span>')

    @property
    def status_badge(self):
        if self.status == 'Aguardando':
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Aguardando</span>')
        if self.status == 'Mov. serviço':
            return mark_safe('<span class="bg-gray-500 text-white px-2 py-1 rounded">Mov. Serviço</span>')
        if self.status == 'Mov. própria':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Mov. Própria</span>')
        if self.status == 'Exclusão a pedido':
            return mark_safe('<span class="bg-indigo-500 text-white px-2 py-1 rounded">Exclusão a Pedido</span>')
        if self.status == 'Tranferido de Unidade':
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Transferido de Unidade</span>')
        if self.status == 'Excluído Alt. quadro':
            return mark_safe('<span class="bg-gray-800 text-white px-2 py-1 rounded">Excluído Alt. Quadro</span>')
        
    @property
    def ultima_imagem(self):
        return self.cadastro.imagens.last()

    def get_status_choices(self):
        return self._meta.get_field('status').choices

    def get_sgb_choices(self):
        return self._meta.get_field('sgb_destino').choices

    def get_posto_secao_choices(self):
        return self._meta.get_field('posto_secao_destino').choices

    def get_alteracao_choices(self):
        return self._meta.get_field('alteracao').choices

class HistoricoRpt(models.Model):
    data_pedido = models.DateField(blank=False, null=False)
    data_movimentacao = models.DateField(blank=True, null=True)  # Opcional
    data_alteracao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50)
    sgb_destino = models.CharField(max_length=50)
    posto_secao_destino = models.CharField(max_length=50)
    doc_solicitacao = models.CharField(max_length=50)
    doc_alteracao = models.CharField(max_length=50, blank=True, null=True)  # Opcional
    doc_movimentacao = models.CharField(max_length=50, blank=True, null=True)  # Opcional
    alteracao = models.CharField(max_length=50,blank=True, null=True)  # Opcional
    cadastro = models.ForeignKey(Cadastro_rpt, related_name='Historicorpt', on_delete=models.CASCADE)
    usuario_alteracao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.cadastro.re} {self.cadastro.dig} {self.cadastro.nome_de_guerra}'
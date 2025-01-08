from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from backend.efetivo.models import Cadastro
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class Cadastro_adicional(models.Model):

    n_choices = [(i, f'{i:02d}') for i in range(1, 9)]

    cadastro = models.OneToOneField(Cadastro, on_delete=models.CASCADE)  # Relacionamento 1-1 com Cadastro
    numero_adicional = models.IntegerField(choices=n_choices, blank=False, null=False)
    data_ultimo_adicional = models.DateField(blank=False, null=False)
    numero_lp = models.IntegerField(choices=n_choices, blank=False, null=False)
    data_ultimo_lp = models.DateField(blank=False, null=False)  
    proximo_adicional = models.DateField(blank=True, null=True)  # Campo para a data calculada
    mes_proximo_adicional = models.IntegerField(blank=True, null=True)
    ano_proximo_adicional = models.IntegerField(blank=True, null=True)
    dias_desconto_adicional = models.IntegerField(default=0)
    proximo_lp = models.DateField(blank=False, null=False)
    mes_proximo_lp = models.IntegerField(blank=False, null=False)
    ano_proximo_lp = models.IntegerField(blank=False, null=False)
    dias_desconto_lp = models.IntegerField(default=0)
    status_adicional = models.CharField(max_length=20, blank=False, null=False)
    status_lp = models.CharField(max_length=20, blank=False, null=False)
    
    
    
    def save(self, *args, **kwargs):
        # Calcular a data do próximo adicional e LP
        if self.data_ultimo_adicional:
            self.proximo_adicional = self.data_ultimo_adicional + relativedelta(years=5)
        if self.data_ultimo_lp:
            self.proximo_lp = self.data_ultimo_lp + relativedelta(years=5)
        
        # Calcular o mês e ano do próximo adicional e LP
        if self.proximo_adicional:
            self.mes_proximo_adicional = self.proximo_adicional.month
            self.ano_proximo_adicional = self.proximo_adicional.year
        if self.proximo_lp:
            self.mes_proximo_lp = self.proximo_lp.month
            self.ano_proximo_lp = self.proximo_lp.year
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.cadastro.re} {self.cadastro.dig} {self.cadastro.nome_de_guerra}'

    def __str__(self):
        return f'{self.cadastro.re} {self.cadastro.dig} {self.cadastro.nome_de_guerra}'

    @property
    def ultima_imagem(self):
        return self.cadastro.imagens.last()

    @property
    def tempo_ats_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.data_ultimo_adicional)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    
        
    def tempo_lp_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.data_ultimo_lp)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    # Adiciona 5 anos à data
    def data_5_anos_adicional(self):
        return self.data_ultimo_adicional + relativedelta(years=5)

    def data_5_anos_lp(self):
        if self.data_ultimo_lp:
            return self.data_ultimo_lp + relativedelta(years=5)
        return None

    # Retorna o mês/ano da data
    def mes_ano(self, data):
        return data.strftime('%m/%Y')

    @property
    def mes_ano_adicional(self):
        return self.mes_ano(self.data_5_anos_adicional())

    @property
    def mes_ano_lp(self):
        if self.data_5_anos_lp():
            return self.mes_ano(self.data_5_anos_lp())
        return None

    # Calcula o total de dias a partir da data até hoje
    def total_dias(self, data):
        hoje = datetime.today().date()
        delta = hoje - data
        return delta.days

    @property
    def total_dias_adicional(self):
        return self.total_dias(self.data_ultimo_adicional)

    @property
    def total_dias_lp(self):
        return self.total_dias(self.data_ultimo_lp)
    
    
    @property
    def ats_status(self):
        dias = self.total_dias_adicional
        if dias >1826:
            return mark_safe('<span class="badge bg-success">Completo</span>')
        if dias >1461:
            return mark_safe('<span class="badge bg-success"> menos de 1 ano</span>')
        if dias > 1095:
            return mark_safe('<span class="badge bg-warning">menos de 2 anos</span>')
        if dias > 730:
            return mark_safe('<span class="badge bg-warning">menos de 3 anos</span>')
        if dias > 365:
            return mark_safe('<span class="badge bg-danger">menos de 4 anos</span>')
        if dias < 365:
            return mark_safe('<span class="badge bg-dark">menos de 5 anos</span>')

        
    @property
    def lp_status(self):
        dias = self.total_dias_lp
        if dias >1826:
            return mark_safe('<span class="badge bg-success">Completo</span>')
        if dias >1461:
            return mark_safe('<span class="badge bg-success"> menos de 1 ano</span>')
        if dias > 1095:
            return mark_safe('<span class="badge bg-warning">menos de 2 anos</span>')
        if dias > 730:
            return mark_safe('<span class="badge bg-warning">menos de 3 anos</span>')
        if dias > 365:
            return mark_safe('<span class="badge bg-danger">menos de 4 anos</span>')
        if dias < 365:
            return mark_safe('<span class="badge bg-dark">menos de 5 anos</span>')

   
    



class Historico_lp_ats(models.Model):
    data_ultimo_adicional = models.DateField(blank=False, null=False)
    data_ultimo_lp = models.DateField(blank=True, null=True)  # Opcional
    cadastro = models.ForeignKey(Cadastro, related_name='historico_lp_ats', on_delete=models.CASCADE)
    usuario_alteracao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return f'{self.cadastro.re} {self.cadastro.dig} {self.cadastro.nome_de_guerra}'
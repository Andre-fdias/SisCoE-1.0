from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from backend.efetivo.models import Cadastro
import locale
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class Cadastro_adicional(models.Model):
    situacao_choices = (
        ("", " "),
        ("Aguardando", "Aguardando"),
        ("Concedido", "Concedido")
    )
    n_choices = [(i, f'{i:02d}') for i in range(1, 9)]

    cadastro = models.OneToOneField(Cadastro, on_delete=models.CASCADE)
    numero_adicional = models.IntegerField(choices=n_choices, blank=False, null=False)
    data_ultimo_adicional = models.DateField(blank=False, null=False)
    numero_lp = models.IntegerField(choices=n_choices, blank=False, null=False)
    data_ultimo_lp = models.DateField(blank=False, null=False)
    numero_prox_adicional = models.IntegerField(choices=n_choices, blank=False, null=False, default=1)
    proximo_adicional = models.DateField(blank=True, null=True)
    mes_proximo_adicional = models.IntegerField(blank=True, null=True)
    ano_proximo_adicional = models.IntegerField(blank=True, null=True)
    dias_desconto_adicional = models.IntegerField(default=0, blank=True, null=True)
    situacao_adicional = models.CharField(choices=situacao_choices, blank=False, null=False, default="Aguardando")
    numero_prox_lp = models.IntegerField(choices=n_choices, blank=False, null=False, default=1)
    proximo_lp = models.DateField(blank=True, null=True)
    mes_proximo_lp = models.IntegerField(blank=True, null=True)
    ano_proximo_lp = models.IntegerField(blank=True, null=True)
    dias_desconto_lp = models.IntegerField(default=0, blank=True, null=True)
    situacao_lp = models.CharField(choices=situacao_choices, blank=False, null=False, default="Aguardando")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Cadastro_adicional.objects.get(pk=self.pk)
            if old_instance.situacao_adicional == "Aguardando" and self.situacao_adicional == "Concedido":
                HistoricoCadastro.objects.create(
                    cadastro=self.cadastro,
                    situacao_adicional=self.situacao_adicional,
                    situacao_lp=self.situacao_lp,
                    usuario_alteracao=self.usuario_alteracao,
                    numero_prox_adicional=self.numero_prox_adicional,
                    proximo_adicional=self.proximo_adicional,
                    mes_proximo_adicional=self.mes_proximo_adicional,
                    ano_proximo_adicional=self.ano_proximo_adicional,
                    dias_desconto_adicional=self.dias_desconto_adicional,
                    numero_prox_lp=self.numero_prox_lp,
                    proximo_lp=self.proximo_lp,
                    mes_proximo_lp=self.mes_proximo_lp,
                    ano_proximo_lp=self.ano_proximo_lp,
                    dias_desconto_lp=self.dias_desconto_lp
                )
        super().save(*args, **kwargs)

    @property
    def ultima_imagem(self):
        return self.cadastro.imagens.last()

    @property
    def status_adicional(self):
        hoje = datetime.today().date()
        if self.proximo_adicional:
            diferenca = (self.proximo_adicional - hoje).days
            if diferenca > 30:
                return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Aguardar</span>')
            elif 0 <= diferenca <= 30:
                return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Lançar</span>')
            else:
                return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">Vencido</span>')
        else:
            return "Data não definida"

    @property
    def status_lp(self):
        hoje = datetime.today().date()
        if self.proximo_lp:
            diferenca = (self.proximo_lp - hoje).days
            if diferenca > 30:
                return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Aguardar</span>')
            elif 0 <= diferenca <= 30:
                return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Lançar</span>')
            else:
                return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">Vencido</span>')
        else:
            return "Data não definida"

    @property
    def mes_abreviado_proximo_adicional(self):
        if self.proximo_adicional:
            meses = {
                1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
            }
            return meses.get(self.proximo_adicional.month, '')
        return None

    @property
    def mes_abreviado_proximo_lp(self):
        if self.proximo_lp:
            meses = {
                1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
            }
            return meses.get(self.proximo_lp.month, '')
        return None

    @property
    def adicional_proximo_lp(self):
        if self.proximo_lp:
            return self.proximo_lp.year
        return None

    @property
    def adicional_proximo_adicional(self):
        if self.proximo_adicional:
            return str(self.proximo_adicional.year)
        return None

    @property
    def tempo_ats_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.data_ultimo_adicional)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def tempo_lp_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.data_ultimo_lp)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

class HistoricoCadastro(models.Model):
    Cadastro_adicional = models.ForeignKey(Cadastro_adicional, on_delete=models.CASCADE)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    situacao_adicional = models.CharField(max_length=20)
    situacao_lp = models.CharField(max_length=20)
    usuario_alteracao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_prox_adicional = models.IntegerField()
    proximo_adicional = models.DateField()
    mes_proximo_adicional = models.IntegerField()
    ano_proximo_adicional = models.IntegerField()
    dias_desconto_adicional = models.IntegerField()
    numero_prox_lp = models.IntegerField()
    proximo_lp = models.DateField()
    mes_proximo_lp = models.IntegerField()
    ano_proximo_lp = models.IntegerField()
    dias_desconto_lp = models.IntegerField()

    def __str__(self):
        return f'Histórico de {self.cadastro} em {self.data_alteracao}'
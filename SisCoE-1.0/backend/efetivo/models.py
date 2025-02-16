from datetime import date, datetime
from backend.accounts.models import User
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from django.core.exceptions import ValidationError
from PIL import Image, ImageDraw, ImageFont
import os
from django.contrib.auth import get_user_model
import locale

try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'C.UTF-8')  # Fallback para locale neutra
    # Ou alternativamente: pass (não altera a locale)

# responsavel pelo cadastro básico de dados de militares

class Cadastro(models.Model):
    genero_choices = (
        ("", " "),
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino")
    )

    alteracao_choices = (
        ("", ""),
        ("Movimentação", "Movimentação"),
        ("Promoção", "Promoção"),
        ("Foto", "Foto"),
        ("Averbação", "Averbação"),
        ("Correção", "Correção"),
        ("Documento", "Documento"),
        ("Contato", "Contato"),
        ("Inclusão", "Inclusão"),
    )
    n_choices = [(i, f'{i:02d}') for i in range(1, 9)]
    
    id = models.AutoField(primary_key=True)
    re = models.CharField(max_length=6,  blank=False, null=False, unique=True)
    dig = models.CharField(max_length=1, blank=False, null=False)
    nome = models.CharField(max_length=50, blank=False, null=False)
    nome_de_guerra = models.CharField(max_length=20, blank=False, null=False)
    genero = models.CharField(max_length=10, blank=False, null=False, choices=genero_choices)
    nasc = models.DateField(blank=False, null=False)
    matricula = models.DateField(blank=False, null=False)
    admissao = models.DateField(blank=False, null=False)
    previsao_de_inatividade = models.DateField(blank=False, null=False)
    cpf = models.CharField(max_length=14, blank=False, null=False, unique=True)
    rg = models.CharField(max_length=14, blank=False, null=False)
    tempo_para_averbar_inss = models.IntegerField(blank=False, null=False, default=1)
    tempo_para_averbar_militar = models.IntegerField(blank=False, null=False, default=1)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    telefone = models.CharField(max_length=14, blank=False, null=False)
    alteracao = models.CharField(max_length=20, blank=False, null=False, choices=alteracao_choices)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cadastros', default=1)  # 
   
  
    def __str__(self):
        return f'{self.re} {self.dig} {self.nome_de_guerra}'

    @property
    def idade_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.nasc)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def matricula_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.matricula)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def admissao_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.admissao)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def previsao_de_inatividade_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(self.previsao_de_inatividade, hoje)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    def previsao_de_inatividade_dias(self):
        hoje = datetime.today().date()
        delta = self.previsao_de_inatividade - hoje
        return delta.days

    def tempo_para_inatividade(self):
        hoje = datetime.now().date()
        diferenca = hoje - self.previsao_de_inatividade
        return diferenca.days

    
    @property
    def inativa_status(self):
        dias = self.previsao_de_inatividade_dias()
        if dias < 1:
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Sim</span>')
        if dias < 180:
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Falta menos de 06 meses</span>')
        if dias < 367:
            return mark_safe('<span class="bg-gray-500 text-white px-2 py-1 rounded">Falta menos de 1 ano</span>')
        return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">Não</span>')
    
    @property
    def tempo_para_averbar_inss_inteiro(self):
        return self.tempo_para_averbar_inss

    @property
    def tempo_para_averbar_militar_inteiro(self):
        return self.tempo_para_averbar_militar
    

    class Meta:
        ordering = ('re',)


class CPF(models.Model):
    id = models.IntegerField(primary_key=True)
    cpf = models.CharField(max_length=14)
    re = models.CharField(max_length=6)

@receiver(post_save, sender=Cadastro)
def create_cpf_record(sender, instance, created, **kwargs):
    if created:
        CPF.objects.create(
            id=instance.id,
            cpf=instance.cpf,
            re=instance.re
        )




# responsavel pelo cadastro sa situação funcional de militares
class DetalhesSituacao(models.Model):

    situacao_choices=(
        ("", " "),
        ("Efetivo","Efetivo"),
        ("Exonerado a Pedido", "Exonerado a Pedido"),
        ("Exonerado Ex-Ofício","Exonerado Ex-Ofício"),
        ("Reserva a Pedido", "Reserva a Pedido"),
        ("Transferido", "Transferido"),
        ("Mov. Interna", "Mov. Interna"),
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

    op_adm_choices=( 
        ("", " "),                                                
        ("Administrativo"," Administrativo"),
        ("Operacional", "Operacional"),
    )


    funcao_choices=(
        ("", " "),
        ("AUX (ADM)" ,"AUX (ADM)" ),
        ("AUX B1" ,"AUX B1" ),
        ("AUX B2" ,"AUX B2" ),
        ("AUX B3" ,"AUX B3" ),
        ("AUX B4" ,"AUX B4" ),
        ("AUX B5" ,"AUX B5" ),
        ("AUXILIARES" ,"AUXILIARES" ),
        ("B.EDUCADOR" ,"B.EDUCADOR" ),
        ("CH DE SETOR" ,"CH DE SETOR" ),
        ("CH SAT" ,"CH SAT" ),
        ("CH SEC ADM" ,"CH SEC ADM" ),
        ("CH_SEÇÃO" ,"CH_SEÇÃO" ),
        ("CMT" ,"CMT" ),
        ("CMT 1ºSGB" ,"CMT 1ºSGB" ),
        ("AUX (MOTOMEC)" ,"AUX (MOTOMEC)" ),
        ("CMT 2ºSGB" ,"CMT 2ºSGB" ),
        ("CMT 3ºSGB" ,"CMT 3ºSGB" ),
        ("CMT 4ºSGB" ,"CMT 4ºSGB" ),
        ("CMT 5ºSGB" ," CMT 5ºSGB" ),
        ("CMT PRONTIDÃO" ,"CMT PRONTIDÃO" ),
        ("CMT_BASE" ,"CMT_BASE" ),
        ("CMT_GB" ,"CMT_GB" ),
        ("CMT_SGB" ,"CMT_SGB" ),
        ("COBOM (ATENDENTE)" ,"COBOM (ATENDENTE)" ),
        ("COBOM (DESPACHADOR)" ,"COBOM (DESPACHADOR)" ),
        ("AUX (NAT)" ,"3 - AUX (NAT)" ),
        ("COBOM (SUPERVISOR)" ,"COBOM (SUPERVISOR)" ),
        ("ESB" ,"ESB" ),
        ("ESSGT" ,"ESSGT" ),
        ("LSV" ,"LSV" ),
        ("LTS" ,"LTS" ),
        ("MECÂNICO" ,"MECÂNICO" ),
        ("MOTORISTA" ,"MOTORISTA" ),
        ("OBRAS" ,"OBRAS" ),
        ("AUX (SAT)" ,"AUX (SAT)" ),
        ("S/FUNÇ_CAD" ,"S/FUNÇ_CAD" ),
        ("TELEFONISTA" ,"TELEFONISTA" ),
        ("TELEMÁTICA" ,"TELEMÁTICA" ),
        ("AUX (SJD)" ,"AUX (SJD)" ),
        ("SUBCMT" ,"SUBCMT" ),
        ("AUX (UGE)" ,"AUX (UGE)" ),
      
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

    esta_adido_choices = (
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

    cat_efetivo_choices=( 
        ("", " "),                                                
        ("ATIVO","ATIVO"),
        ("INATIVO","INATIVO"),
        ("LSV", "LSV"),
        ("LTS", "LTS"),
        ("LTS FAMILIA", "LTS FAMILIA"),
        ("CONVAL", "CONVAL"),
        ("ELEIÇÃO", "ELEIÇAO"),
        ("LP", "LP"),
        ("FERIAS", "FÉRIAS"),
    )

    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE,
                                 related_name='detalhes_situacao')
    situacao = models.CharField(max_length=30, blank=False, null=False, choices=cat_efetivo_choices,    default="Efetivo")
    cat_efetivo = models.CharField(max_length=30, blank=False, null=False, choices=situacao_choices,    default="Ativo")
    sgb = models.CharField(max_length=9, blank=False, null=False, choices=sgb_choices)
    posto_secao = models.CharField(max_length=100, blank=False, null=False, choices=posto_secao_choices)
    esta_adido = models.CharField(max_length=100, blank=True, null=True, choices=esta_adido_choices)
    funcao = models.CharField(max_length=50, blank=False, null=False, choices=funcao_choices)
    op_adm = models.CharField(max_length=18, blank=False, null=False, choices=op_adm_choices)
    apresentacao_na_unidade = models.DateField(blank=False, null=False)
    saida_da_unidade = models.DateField(blank=True, null=True)
    data_alteracao  = models.DateTimeField(auto_now_add=True)
    usuario_alteracao = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
      return f'{self.cadastro.re} - {self.situacao}'
    
    @property
    def tempo_na_unidade(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.apresentacao_na_unidade)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"

    
    
    @property
    def status(self):
        if self.situacao == 'Efetivo':
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Efetivo</span>')
        if self.situacao == 'Exonerado a Pedido':
            return mark_safe('<span class="bg-gray-500 text-white px-2 py-1 rounded">Exonerado a Pedido</span>')
        if self.situacao == 'Exonerado Ex-Ofício':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Exonerado Ex-Ofício</span>')
        if self.situacao == 'Reserva a Pedido':
            return mark_safe('<span class="bg-indigo-500 text-white px-2 py-1 rounded">Reserva a Pedido</span>')
        if self.situacao == 'Transferido':
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Transferido</span>')
        if self.situacao == 'Mov. Interna':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Mov. Interna</span>')
     

 
    @property
    def status_cat(self):
        if self.cat_efetivo == 'ATIVO':
            return mark_safe('<span class="bg-green-500 text-white px-2 py-1 rounded">Ativo</span>')
        if self.cat_efetivo == 'INATIVO':
            return mark_safe('<span class="bg-gray-500 text-white px-2 py-1 rounded">Inativo</span>')
        if self.cat_efetivo == 'LSV':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Lsv</span>')
        if self.cat_efetivo == 'LTS':
            return mark_safe('<span class="bg-indigo-500 text-white px-2 py-1 rounded">Lts</span>')
        if self.cat_efetivo == 'LTS FAMILIA':
            return mark_safe('<span class="bg-yellow-500 text-white px-2 py-1 rounded">Lts Familia</span>')
        if self.cat_efetivo == 'CONVAL':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Conval</span>')
        if self.cat_efetivo == 'ELEIÇÃO':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Eleição</span>')
        if self.cat_efetivo == 'LP':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">LP</span>')
        if self.cat_efetivo == 'FERIAS':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Férias</span>')


# responsavel pelas promoções de militares

class Promocao(models.Model):
    posto_grad_choices =(
      ("", " "),
      ("Cel PM", "Cel PM"),
      ("Ten Cel PM", "Ten Cel PM"),
      ("Maj PM", "Maj PM"),
      ("CAP PM", "Cap PM"),
      ("1º Ten PM", "1º Ten PM"),
      ("1º Ten QAPM", "1º Ten QAOPM"),
      ("2º Ten PM", "2º Ten PM"),
      ("2º Ten QAPM", "2º Ten QAOPM"),
      ("Asp OF PM", "Asp OF PM"),
      ("Subten PM", "Subten PM"),
      ("1º Sgt PM", "1º Sgt PM"),
      ("2º Sgt PM", "2º Sgt PM"),
      ("3º Sgt PM", "3º Sgt PM"),
      ("Cb PM", "Cb PM"),
      ("Sd PM", "Sd PM"),
      ("Sd PM 2ºCL", "Sd PM 2ºCL"),
   )


    quadro_choices=(
      ("", " "),
      ("Oficiais", "Oficiais"),
      ("Praças Especiais" ,"Praças Especiais"),
      ( "Praças", "Praças")
   )

    grupo_choices=( 
      ("", " "),                                                
      ("Cel"," Cel"),
      ("Tc", "Tc"),
      ("Maj", "Maj"),
      ("Cap", "Cap"),
      ("Ten", "Ten"),
      ("Ten QAOPM", "Ten QAOPM"),
      ("Praça Especiais","Praça Especiais"),
      ("St/Sgt", "St/Sgt"),
      ("Cb/Sd", "Cb/Sd")
    )  
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='promocoes')
    posto_grad = models.CharField(max_length=100, choices=posto_grad_choices)
    quadro = models.CharField(max_length=100, choices=quadro_choices)
    grupo = models.CharField(max_length=100, choices=grupo_choices)
    ultima_promocao = models.DateField(blank=False, null=False)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.cadastro} - {self.posto_grad}'

    @property
    def grad(self):
        if self.posto_grad == 'Cel PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Cel PM</span>')
        if self.posto_grad == 'Ten Cel PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Ten Cel PM</span>')
        if self.posto_grad == 'Maj PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Maj PM</span>')
        if self.posto_grad == 'CAP PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">CAP PM</span>')
        if self.posto_grad == '1º Ten PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">1º Ten PM</span>')
        if self.posto_grad == '1º Ten QAPM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">1º Ten QAPM</span>')
        if self.posto_grad == '2º Ten PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">2º Ten PM</span>')
        if self.posto_grad == '2º Ten QAPM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">2º Ten QAPM</span>')
        if self.posto_grad == 'Asp OF PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Asp OF PM</span>')
        if self.posto_grad == 'Subten PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">Subten PM</span>')
        if self.posto_grad == '1º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">1º Sgt PM</span>')
        if self.posto_grad == '2º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">2º Sgt PM</span>')
        if self.posto_grad == '3º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">3º Sgt PM</span>')
        if self.posto_grad == 'Cb PM':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Cb PM</span>')
        if self.posto_grad == 'Sd PM':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Sd PM</span>')
        if self.posto_grad == 'Sd PM 2ºCL':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Sd PM 2ºCL</span>')
   
    @property
    def ultima_promocao_detalhada(self):
        hoje = datetime.today()
        delta = relativedelta(hoje, self.ultima_promocao)
        return f"{delta.years} anos, {delta.months} meses e {delta.days} dias"




from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.efetivo.utils import add_cpf_to_image  # Importe a função

class Imagem(models.Model):
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='imagens')
    image = models.ImageField(upload_to='img/fotos_perfil')
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Imagem de {self.cadastro.nome_de_guerra}'

@receiver(post_save, sender=Imagem)
def add_cpf_to_profile_image(sender, instance, **kwargs):
    cpf = instance.cadastro.cpf
    image_path = instance.image.path
    output_path = os.path.join(os.path.dirname(image_path), f"cpf_{os.path.basename(image_path)}")
    add_cpf_to_image(image_path, cpf, output_path)
    instance.image = output_path
    instance.save()
# modelo de dados para  gerar o historico de promoções  do militar


class HistoricoPromocao(models.Model):
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    posto_grad = models.CharField(max_length=100)
    quadro = models.CharField(max_length=100)
    grupo = models.CharField(max_length=100)
    ultima_promocao = models.DateField()
    data_alteracao = models.DateTimeField(auto_now_add=True) 
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.cadastro.re} - {self.posto_grad}'


# modelo de dados para  gerar o historico de movimentações  do militar


class HistoricoDetalhesSituacao(models.Model):
    cadastro = models.ForeignKey(Cadastro, on_delete=models.CASCADE)
    situacao = models.CharField(max_length=50)
    sgb = models.CharField(max_length=50)
    posto_secao = models.CharField(max_length=50)
    esta_adido = models.CharField(max_length=50)
    funcao = models.CharField(max_length=50)
    op_adm = models.CharField(max_length=50)
    cat_efetivo = models.CharField(max_length=30, blank=False, null=False,  default="Efetivo")
    apresentacao_na_unidade = models.DateField()
    saida_da_unidade = models.DateField(null=True, blank=True)
    data_alteracao = models.DateTimeField(auto_now_add=True)
    usuario_alteracao = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return f' {self.situacao}'


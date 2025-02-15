from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model




User = get_user_model()

class Cadastro_bm(models.Model):

    genero_choices = (
        ("", " "),
        ("Masculino", "Masculino"),
        ("Feminino", "Feminino")
    )

    alteracao_choices = (
        ("", ""),
        ("Movimentação", "Movimentação"),
        ("Foto", "Foto"),
        ("Correção", "Correção"),
        ("Documento", "Documento"),
        ("Contato", "Contato"),
        ("Inclusão", "Inclusão"),
    )

    situacao_choices=(
        ("", " "),
        ("Efetivo","Efetivo"),
        ("Exonerado a Pedido", "Exonerado a Pedido"),
        ("Exonerado Ex-Ofício","Exonerado Ex-Ofício"),
        ("Reserva a Pedido", "Reserva a Pedido"),
        ("Transferido", "Transferido"),

       )
    sgb_choices=( 
        ("", " "),                                                
        ("1ºSGB", "1ºSGB"),
        ("2ºSGB", "2ºSGB"),
        ("3ºSGB", "3ºSGB"),
        ("4ºSGB", "4ºSGB"),
        ("5ºSGB", "5ºSGB")
    )
    
    funcao_choices=(
        ("", " "),
        ("AUX (ADM)" ,"AUX (ADM)" ),
        ("AUXILIARES" ,"AUXILIARES" ),
        ("TELEGRAFISTA" ,"TELEGRAFISTA" ),
        ("MOTORISTA" ,"MOTORISTA" ),
       
    )
    posto_secao_choices = (
         ("", " "),
         ("703151101 - EB CERRADO", "EB CERRADO"),
         ("703151102 - EB ZONA NORTE", "EB ZONA NORTE"),
         ("703151201 - EB SANTA ROSÁLIA", "EB SANTA ROSÁLIA"),
         ("703151202 - EB ÉDEM", "EB ÉDEM"),
         ("703151301 - EB VOTORANTIM", "EB VOTORANTIM"),
         ("703151302 - EB PIEDADE", "EB PIEDADE"),
         ("703152101 - EB ITU", "EB ITU"),
         ("703152102 - EB PORTO FELIZ", "EB PORTO FELIZ"),
         ("703152201 - EB SALTO", "EB SALTO"),
         ("703152301 - EB SÃO ROQUE", "EB SÃO ROQUE"),
         ("703152302 - EB IBIÚNA", "EB IBIÚNA"),
         ("703153101 - EB ITAPEVA", "EB ITAPEVA"),
         ("703153102 - EB APIAÍ", "EB APIAÍ"),
         ("703153103 - EB ITARARÉ", "EB ITARARÉ"),
         ("703153104 - EB CAPÃO BONITO", "EB CAPÃO BONITO"),
         ("703154101 - EB ITAPETININGA", "EB ITAPETININGA"),
         ("703154102 - EB BOITUVA", "EB BOITUVA"),
         ("703154103 - EB ANGATUBA", "EB ANGATUBA"),
         ("703154201 - EB TATUÍ", "EB TATUÍ"),
         ("703154202 - EB TIETÊ", "EB TIETÊ"),
         ("703154203 - EB LARANJAL PAULISTA", "EB LARANJAL PAULISTA"),
         ("703155101 - EB BOTUCATU", "EB BOTUCATU"),
         ("703155102 - EB ITATINGA", "EB ITATINGA"),
         ("703155201 - EB AVARÉ", "EB AVARÉ"),
         ("703155202 - EB PIRAJU", "EB PIRAJU"),
         ("703155203 - EB ITAÍ", "EB ITAÍ"),
      )
    esb_choices=( 
        ("", " "),                                                
        ("SIM", "SIM"),
        ("NÃO", "NÃO"),
       
    )
    ovb_choices=( 
        ("", " "),                                                
        ("LEVE", "LEVE"),
        ("PESADO", "PESADO"),
        ("NÃO POSSUI", "NÃO POSSUI"),
    )
    cat_cnh_choices=( 
        ("", " "),                                                
        ("A", "A"),
        ("AB", "AB"),
        ("AC", "AC "),                                                
        ("AD", "AD"),
        ("AE", "AE"),
        ("B", " B"),                                                
        ("C", "C"),
        ("D", "D"),
        ("E", "E"),
    )
    

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, blank=False, null=False)
    nome_de_guerra = models.CharField(max_length=20, blank=False, null=False)
    situacao = models.CharField(max_length=30, blank=False, null=False, choices=situacao_choices, default="Efetivo")
    sgb = models.CharField(max_length=9, blank=False, null=False, choices=sgb_choices)
    posto_secao = models.CharField(max_length=100, blank=False, null=False, choices=posto_secao_choices)
    cpf = models.CharField(max_length=14, blank=False, null=False, unique=True)
    rg = models.CharField(max_length=14, blank=False, null=False)
    cnh = models.CharField(max_length=14, blank=False, null=False)
    cat_cnh = models.CharField(max_length=4, blank=False, null=False, choices=cat_cnh_choices)
    esb = models.CharField(max_length=4, blank=False, null=False, choices=esb_choices)
    ovb = models.CharField(max_length=10, blank=False, null=False, choices=ovb_choices)
    admissao = models.DateField(blank=False, null=False)
    nasc = models.DateField(blank=False, null=False)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=14, blank=False, null=False)
    apresentacao_na_unidade = models.DateField(blank=False, null=False)
    saida_da_unidade = models.DateField(blank=True, null=True)
    funcao = models.CharField(max_length=50, blank=False, null=False, choices=funcao_choices)
    data_alteracao = models.DateTimeField(auto_now=True)
    usuario_alteracao = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    genero = models.CharField(max_length=10, blank=False, null=False, choices=genero_choices)
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cadastros_bm', default=1)
    def __str__(self):
        return f'{self.nome}'

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

    def apresentacao_detalhada(self):
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
       


class Imagem_bm(models.Model):
    cadastro = models.ForeignKey(Cadastro_bm, on_delete=models.CASCADE, related_name='imagens')
    image = models.ImageField(upload_to='img/fotos_bm')
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'Imagem de {self.cadastro.nome_de_guerra}'
    
from django.db import models
#from geopy.distance import geodesic


class Municipios(models.Model):

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

    cidade_posto_choices = [
    ("Avaré", "Avaré"),
    ("Apiaí", "Apiaí"),
    ("Itapetininga", "Itapetininga"),
    ("Itararé", "Itararé"),
    ("São Roque", "São Roque"),
    ("Capão Bonito", "Capão Bonito"),
    ("Sorocaba", "Sorocaba"),
    ("Angatuba", "Angatuba"),
    ("Botucatu", "Botucatu"),
    ("Itaí", "Itaí"),
    ("Boituva", "Boituva"),
    ("Tatuí", "Tatuí"),
    ("Tietê", "Tietê"),
    ("Laranjal Paulista", "Laranjal Paulista"),
    ("Piraju", "Piraju"),
    ("Ibiúna", "Ibiúna"),
    ("Itapeva", "Itapeva"),
    ("Itatinga", "Itatinga"),
    ("Itu", "Itu"),
    ("Piedade", "Piedade"),
    ("Porto Feliz", "Porto Feliz"),
    ("Salto", "Salto"),
    ("Votorantim", "Votorantim"),
    ("São Paulo", "São Paulo"),
]
    posto_atendimento_choices = [
    ("EB AVARÉ", "EB AVARÉ"),
    ("EB APIAÍ", "EB APIAÍ"),
    ("EB ITAPETININGA", "EB ITAPETININGA"),
    ("EB ITARARÉ", "EB ITARARÉ"),
    ("EB SÃO ROQUE", "EB SÃO ROQUE"),
    ("EB CAPÃO BONITO", "EB CAPÃO BONITO"),
    ("EB CERRADO", "EB CERRADO"),
    ("EB ANGATUBA", "EB ANGATUBA"),
    ("EB BOTUCATU", "EB BOTUCATU"),
    ("EB SALTO", "EB SALTO"),
    ("EB ITAÍ", "EB ITAÍ"),
    ("EB BOITUVA", "EB BOITUVA"),
    ("EB TATUÍ", "EB TATUÍ"),
    ("EB TIETÊ", "EB TIETÊ"),
    ("EB LARANJAL PAULISTA", "EB LARANJAL PAULISTA"),
    ("EB PIRAJU", "EB PIRAJU"),
    ("EB IBIÚNA", "EB IBIÚNA"),
    ("EB ITAPEVA", "EB ITAPEVA"),
    ("EB ITATINGA", "EB ITATINGA"),
    ("EB ITU", "EB ITU"),
    ("EB PIEDADE", "EB PIEDADE"),
    ("EB PORTO FELIZ", "EB PORTO FELIZ"),
    ("EB VOTORANTIM", "EB VOTORANTIM"),
    ("ESSgt", "ESSgt"),
    ("EB SANTA ROSÁLIA", "EB SANTA ROSÁLIA"),
    ("EB ZONA NORTE", "EB ZONA NORTE"),
    ("EB ÉDEM", "EB ÉDEM"),
    ("LTS", "LTS"),
    ("LSV", "LSV"),
]
    
    tipo_choices=( 
        ("", " "),                                                
        ("Sede","Sede"),
        ("Apoio", "Apoio"),
    )
    id = models.AutoField(primary_key=True)

    sgb = models.CharField(max_length=9, blank=False, null=False, choices=sgb_choices)
    posto_secao = models.CharField(max_length=100, blank=False, null=False, choices=posto_secao_choices)
   
    posto_atendimento = models.CharField(max_length=9, blank=False, null=False, choices=posto_atendimento_choices)
    cidade_posto = models.CharField(max_length=9, blank=False, null=False, choices=cidade_posto_choices)
    tipo_cidade = models.CharFieldmax_length=9, blank=False, null=False, choices=op_adm_choices)
    operacional_ou_adm = models.CharFieldmax_length=9, blank=False, null=False, choices=tipo_choices)
    municipio = models.CharField(max_length=100)   
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
    cel = models.IntegerField(blank=False, null=False)
    ten_cel= models.IntegerField(blank=False, null=False)
    maj= models.IntegerField(blank=False, null=False)
    cap = models.IntegerField(blank=False, null=False)
    ten= models.IntegerField(blank=False, null=False)
    ten_qa= models.IntegerField(blank=False, null=False)
    st_sgt= models.IntegerField(blank=False, null=False)
    cb/sd= models.IntegerField(blank=False, null=False)
    
    bandeira = models.URLField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.posto_atendimento
    


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

    #def distancia_para(self, outro_endereco):
    #   """Calcula a distância para outro endereço em quilômetros."""
    #  origem = (self.latitude, self.longitude)
    # destino = (outro_endereco.latitude, outro_endereco.longitude)
    # return geodesic(origem, destino).kilometers
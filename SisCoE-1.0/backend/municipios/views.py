from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Posto, Contato, Pessoal,Cidade

from django.shortcuts import render, get_object_or_404
from .models import Posto

def posto_list(request):
    postos = Posto.objects.all().prefetch_related('pessoal', 'cidades')
    cidades = Cidade.objects.all().select_related('posto')  # Novo queryset
    return render(request, 'posto_list.html', {
        'postos': postos,
        'cidades': cidades  # Adicionar ao contexto
    })

def posto_detail(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    return render(request, 'posto_detail.html', {'posto': posto})


def municipio_detail(request, pk):
    cidade = get_object_or_404(Cidade, pk=pk)
    posto = cidade.posto  # Obtenha o posto relacionado à cidade
    return render(request, 'municipio_detail.html', {'cidade': cidade, 'posto': posto})

def posto_secao_detail(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    return render(request, 'posto_secao_detail.html', {'posto': posto})


def posto_create(request):
    sgb_choices = Posto.sgb_choices
    posto_secao_choices = Posto.posto_secao_choices
    posto_atendimento_choices = Posto.posto_atendimento_choices
    cidade_posto_choices = Posto.cidade_posto_choices
    municipio_choices = Cidade.municipio_choices
    tipo_choices = Posto.tipo_choices
    op_adm_choices = Posto.op_adm_choices

    if request.method == 'POST':
        # Dados do Posto
        posto_data = {
            'sgb': request.POST.get('sgb'),
            'posto_secao': request.POST.get('posto_secao'),
            'posto_atendimento': request.POST.get('posto_atendimento'),
            'cidade_posto': request.POST.get('cidade_posto'),
            'tipo_cidade': request.POST.get('tipo_cidade'),
            'op_adm': request.POST.get('op_adm'),
            'usuario': request.user,
            'quartel': request.FILES.get('quartel')
            }
        
        # Cria o Posto
        posto = Posto.objects.create(**posto_data)

        # Dados do Contato
        contato_data = {
            'posto': posto,
            'telefone': request.POST.get('telefone'),
            'rua': request.POST.get('rua'),
            'numero': request.POST.get('numero'),
            'complemento': request.POST.get('complemento'),
            'bairro': request.POST.get('bairro'),
            'cidade': request.POST.get('cidade'),
            'cep': request.POST.get('cep'),
            'email': request.POST.get('email_funcional'),
            'latitude': request.POST.get('latitude_contato'),
            'longitude': request.POST.get('longitude_contato'),
        }
        Contato.objects.create(**contato_data)

        # Dados do Pessoal
        pessoal_data = {
            'posto': posto,
            'cel': int(request.POST.get('cel', 0)),
            'ten_cel': int(request.POST.get('ten_cel', 0)),
            'maj': int(request.POST.get('maj', 0)),
            'cap': int(request.POST.get('cap', 0)),
            'tenqo': int(request.POST.get('ten', 0)),  # Corrigido para match com o template
            'tenqa': int(request.POST.get('tenqa', 0)),
            'asp': int(request.POST.get('asp', 0)),
            'st_sgt': int(request.POST.get('st_sgt', 0)),
            'cb_sd': int(request.POST.get('cb_sd', 0)),
        }
        Pessoal.objects.create(**pessoal_data)

        # Dados das Cidades (múltiplas entradas)
        municipios = request.POST.getlist('municipios[]')
        latitudes = request.POST.getlist('latitudes[]')
        longitudes = request.POST.getlist('longitudes[]')
        bandeiras = request.FILES.getlist('bandeiras[]')
        descricoes = request.POST.getlist('descricoes[]')
       
        for i in range(len(municipios)):
            Cidade.objects.create(
                posto=posto,
                municipio=municipios[i],
                descricao=descricoes[i],  # Nova linha
                latitude=latitudes[i],
                longitude=longitudes[i],
                bandeira=bandeiras[i] if i < len(bandeiras) else None
            )

        return redirect('municipios:posto_list')

    return render(request, 'posto_form.html', {
        'sgb_choices': sgb_choices,
        'posto_secao_choices': posto_secao_choices,
        'posto_atendimento_choices': posto_atendimento_choices,
        'cidade_posto_choices': cidade_posto_choices,
        'municipio_choices': municipio_choices,
        'tipo_choices': tipo_choices,
        'op_adm_choices': op_adm_choices
    })

def posto_update(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    sgb_choices = Posto.sgb_choices
    posto_secao_choices = Posto.posto_secao_choices
    posto_atendimento_choices = Posto.posto_atendimento_choices
    cidade_posto_choices = Posto.cidade_posto_choices
    tipo_choices = Posto.tipo_choices
    op_adm_choices = Posto.op_adm_choices

    if request.method == 'POST':
        # Atualiza o Posto
        posto.sgb = request.POST.get('sgb')
        posto.posto_secao = request.POST.get('posto_secao')
        posto.posto_atendimento = request.POST.get('posto_atendimento')
        posto.cidade_posto = request.POST.get('cidade_posto')
        posto.tipo_cidade = request.POST.get('tipo_cidade')
        posto.op_adm = request.POST.get('op_adm')
        if request.FILES.get('quartel'):
            posto.quartel = request.FILES.get('quartel')
        posto.save()

        # Atualiza Contato
        contato = posto.contato
        if contato:
            contato.telefone = request.POST.get('telefone')
            contato.rua = request.POST.get('rua')
            contato.numero = request.POST.get('numero')
            contato.complemento = request.POST.get('complemento')
            contato.bairro = request.POST.get('bairro')
            contato.cidade = request.POST.get('cidade')
            contato.cep = request.POST.get('cep')
            contato.email = request.POST.get('email')
            contato.latitude = request.POST.get('latitude')
            contato.longitude = request.POST.get('longitude')
            contato.save()

        # Atualiza Pessoal
        pessoal = posto.pessoal.first()
        if pessoal:
            pessoal.cel = int(request.POST.get('cel', 0))
            pessoal.ten_cel = int(request.POST.get('ten_cel', 0))
            pessoal.maj = int(request.POST.get('maj', 0))
            pessoal.cap = int(request.POST.get('cap', 0))
            pessoal.tenqo = int(request.POST.get('tenqo', 0))
            pessoal.tenqa = int(request.POST.get('tenqa', 0))
            pessoal.asp = int(request.POST.get('asp', 0))
            pessoal.st_sgt = int(request.POST.get('st_sgt', 0))
            pessoal.cb_sd = int(request.POST.get('cb_sd', 0))
            pessoal.save()

        # Atualiza Cidades
        posto.cidades.all().delete()  # Remove as cidades antigas
        municipios = request.POST.getlist('municipios[]')
        latitudes = request.POST.getlist('latitudes[]')
        longitudes = request.POST.getlist('longitudes[]')
        bandeiras = request.FILES.getlist('bandeiras[]')
        descricoes = request.POST.getlist('descricoes[]')

        for i in range(len(municipios)):
            Cidade.objects.create(
                posto=posto,
                municipio=municipios[i],
                descricao=descricoes[i],
                latitude=latitudes[i],
                longitude=longitudes[i],
                bandeira=bandeiras[i] if i < len(bandeiras) else None
            )

        return redirect('municipios:posto_list')

    # Carrega dados existentes para edição
    contato = posto.contato
    pessoal = posto.pessoal.first()
    cidades = posto.cidades.all()

    return render(request, 'posto_form.html', {
        'posto': posto,
        'contato': contato,
        'pessoal': pessoal,
        'cidades': [{
            'municipio': cidade.municipio,
            'descricao': cidade.descricao,
            'latitude': cidade.latitude,
            'longitude': cidade.longitude,
            'bandeira': cidade.bandeira
        } for cidade in cidades],
        'sgb_choices': sgb_choices,
        'posto_secao_choices': posto_secao_choices,
        'posto_atendimento_choices': posto_atendimento_choices,
        'cidade_posto_choices': cidade_posto_choices,
        'tipo_choices': tipo_choices,
        'op_adm_choices': op_adm_choices
    })




def posto_delete(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    if request.method == 'POST':
        posto.delete()
        return redirect('posto_list')
    return render(request, 'posto_confirm_delete.html', {'posto': posto})
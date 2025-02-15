from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from backend.efetivo.models import Cadastro, DetalhesSituacao, Promocao, Imagem  # Ajuste a importaÃ§Ã£o conforme necessÃ¡rio
from datetime import datetime
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Cadastro_adicional, HistoricoCadastro


# Cadastra um novo registro de adicional/LP para um militar

@login_required
def cadastrar_lp(request):
    if request.method == 'GET':
        return render(request, 'cadastrar_lp.html')

    elif request.method == 'POST':
        n_bloco_adicional = request.POST.get('n_bloco_adicional')
        n_bloco_lp = request.POST.get('n_bloco_lp')
        cadastro_id = request.POST.get('cadastro_id')
        data_ultimo_adicional = request.POST.get('data_ultimo_adicional')
        data_ultimo_lp = request.POST.get('data_ultimo_lp')
        user=request.user,  # Garantindo que o usuário esteja sendo atribuído
        
        if not cadastro_id:
            messages.add_message(request, messages.ERROR, 'Cadastro do militar não localizado', extra_tags='bg-green-500 text-white p-4 rounded')
            return redirect('cadastrar_lp')

        cadastro = get_object_or_404(Cadastro, id=cadastro_id)

        if not data_ultimo_adicional:
            messages.add_message(request, messages.ERROR, 'Favor inserir a data de concessão do último Adicional', extra_tags='bg-green-500 text-white p-4 rounded')
            return redirect('cadastrar_lp')

        if not data_ultimo_lp:
            messages.add_message(request, messages.ERROR, 'Favor inserir a data de concessão da última LP', extra_tags='bg-green-500 text-white p-4 rounded')
            return redirect('cadastrar_lp')

        cadastro_adicional = Cadastro_adicional.objects.create(
            cadastro=cadastro,
            numero_adicional=n_bloco_adicional,
            numero_lp=n_bloco_lp,
            data_ultimo_adicional=data_ultimo_adicional,
            data_ultimo_lp=data_ultimo_lp,
            user=user,  # Adicionando o usuário que fez a alteração
            situacao_adicional="Aguardando",
            situacao_lp="Aguardando"
        )
        messages.add_message(request, messages.SUCCESS, 'Adicional e LP cadastrados com Sucesso', extra_tags='bg-green-500 text-white p-4 rounded')
        return redirect(reverse('adicional:listar_lp'))
    return render(request, 'cadastrar_lp.html')

# Lista todos os registros de adicionais/LPs

@login_required
def listar_lp(request):
    registros_adicional = Cadastro_adicional.objects.exclude(data_ultimo_adicional__isnull=True)
    registros_lp = Cadastro_adicional.objects.exclude(data_ultimo_lp__isnull=True)
    
    current_year = datetime.now().year
    anos = list(range(2018, current_year + 2))  # Inclui o próximo ano

    context = {
        'registros_adicional': registros_adicional,
        'registros_lp': registros_lp,
        'anos': anos,
    }
    
    return render(request, 'listar_lp.html', context)



# Exibe os detalhes de um registro especÃ­fico
@login_required
def ver_lp(request, id):
    cadastro_adicional = get_object_or_404(Cadastro_adicional, id=id)
    context = {
        'cadastro': cadastro_adicional
    }
    return render(request, 'ver_lp.html', context)




# Edita um registro existente@login_required
@login_required
def editar_lp(request, id):
    cadastro_adicional = get_object_or_404(Cadastro_adicional, id=id)

    if request.method == 'POST':
        if 'numero_adicional' in request.POST:
            cadastro_adicional.numero_adicional = request.POST.get('numero_adicional')
            cadastro_adicional.data_ultimo_adicional = request.POST.get('data_ultimo_adicional')
            cadastro_adicional.numero_prox_adicional = request.POST.get('numero_prox_adicional')
            cadastro_adicional.proximo_adicional = request.POST.get('proximo_adicional')
            cadastro_adicional.situacao_adicional = request.POST.get('situacao_adicional')
        if 'numero_lp' in request.POST:
            cadastro_adicional.numero_lp = request.POST.get('numero_lp')
            cadastro_adicional.data_ultimo_lp = request.POST.get('data_ultimo_lp')
            cadastro_adicional.numero_prox_lp = request.POST.get('numero_prox_lp')
            cadastro_adicional.proximo_lp = request.POST.get('proximo_lp')
            cadastro_adicional.situacao_lp = request.POST.get('situacao_lp')
        
        cadastro_adicional.save()
        messages.add_message(request, messages.SUCCESS, 'Cadastro atualizado com sucesso', extra_tags='bg-green-500 text-white p-4 rounded')
        return redirect(reverse('adicional:ver_lp', args=[id]))

    context = {
        'cadastro': cadastro_adicional
    }
    return render(request, 'editar_lp.html', context)

# Exclui um registro
@login_required
def excluir_lp(request, id):
    cadastro = get_object_or_404(Cadastro_adicional, id=id)
    if request.method == 'POST':
        cadastro.delete()
        messages.add_message(request, constants.SUCCESS, 'Adicional e LP excluídos com Sucesso', extra_tags='bg-green-500 text-white p-4 rounded')
        return redirect('listar_adicional')
    return redirect('listar_adicional')



# Busca um militar por seu nÃºmero de registro (RE) e preenche o formulÃ¡rio
@login_required
def buscar_militar2(request):
    if request.method == "POST":
        re = request.POST.get('re')
        try:
            cadastro = Cadastro.objects.get(re=re)
            detalhes = DetalhesSituacao.objects.filter(cadastro=cadastro).order_by('-id').first()
            imagem = Imagem.objects.filter(cadastro=cadastro).order_by('-id').first()
            promocao = Promocao.objects.filter(cadastro=cadastro).order_by('-id').first()

            if not detalhes:
                messages.add_message(request, constants.ERROR, 'Detalhamento não encontrado', extra_tags='bg-green-500 text-white p-4 rounded')
                return redirect('adicional:cadastrar_lp')
            if not promocao:
                messages.add_message(request, constants.ERROR, 'Dados de Posto e graduação não localizados', extra_tags='bg-green-500 text-white p-4 rounded')
                return redirect('adicional:cadastrar_lp')

            context = {
                'cadastro': cadastro,
                'detalhes': detalhes,
                'imagem': imagem,
                'promocao': promocao,
            }
            return render(request, 'cadastrar_lp.html', context)
        except Cadastro.DoesNotExist:
            messages.add_message(request, constants.ERROR, 'Militar não cadastrado no sistema', extra_tags='bg-green-500 text-white p-4 rounded')
            return redirect('adicional:cadastrar_lp')

    return render(request, 'buscar_adicional.html')

def gravar_historico(cadastro_adicional, usuario_alteracao):
    HistoricoCadastro.objects.create(
        cadastro=cadastro_adicional.cadastro,
        situacao_adicional=cadastro_adicional.situacao_adicional,
        situacao_lp=cadastro_adicional.situacao_lp,
        usuario_alteracao=usuario_alteracao,
        numero_prox_adicional=cadastro_adicional.numero_prox_adicional,
        proximo_adicional=cadastro_adicional.proximo_adicional,
        mes_proximo_adicional=cadastro_adicional.mes_proximo_adicional,
        ano_proximo_adicional=cadastro_adicional.ano_proximo_adicional,
        dias_desconto_adicional=cadastro_adicional.dias_desconto_adicional,
        numero_prox_lp=cadastro_adicional.numero_prox_lp,
        proximo_lp=cadastro_adicional.proximo_lp,
        mes_proximo_lp=cadastro_adicional.mes_proximo_lp,
        ano_proximo_lp=cadastro_adicional.ano_proximo_lp,
        dias_desconto_lp=cadastro_adicional.dias_desconto_lp
    )

@login_required
def historico_lp(request, id):
    cadastro_adicional = get_object_or_404(Cadastro_adicional, id=id)
    historicos = HistoricoCadastro.objects.filter(cadastro=cadastro_adicional.cadastro).order_by('-data_alteracao')
    context = {
        'historicos': historicos
    }
    return render(request, 'historico_lp.html', context)
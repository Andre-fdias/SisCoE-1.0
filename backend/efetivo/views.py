from django.shortcuts import render, redirect, get_object_or_404
from .models import Cadastro, DetalhesSituacao, Promocao, Imagem, HistoricoDetalhesSituacao, HistoricoPromocao
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from django.db import IntegrityError



# responsavel pelo cadastro  de militares, feito atraves da página cadastrar_militar.html

def cadastrar_militar(request):
    if request.method == "GET":
        context = {
            'posto_grad': Promocao.posto_grad_choices,
            'quadro': Promocao.quadro_choices,
            'grupo': Promocao.grupo_choices,
            'sgb': DetalhesSituacao.sgb_choices,
            'posto_secao': DetalhesSituacao.posto_secao_choices,
            'esta_adido': DetalhesSituacao.esta_adido_choices,
            'funcao': DetalhesSituacao.funcao_choices,
            'op_adm': DetalhesSituacao.op_adm_choices,
            'genero': Cadastro.genero_choices,
            'situacao': DetalhesSituacao.situacao_choices,
            'cat_efetivo': DetalhesSituacao.cat_efetivo_choices,
        }
        return render(request, 'cadastrar_militar.html', context)

    elif request.method == "POST":
        print("Dados recebidos no POST:")
        print(request.POST)

        cpf = request.POST.get('cpf')
        if Cadastro.objects.filter(cpf=cpf).exists():
            messages.add_message(request, constants.ERROR, 'Erro: CPF já cadastrado.')
            return redirect('/efetivo/cadastrar_militar')

        try:
            cadastro = Cadastro(
                re=request.POST.get('re'),
                dig=request.POST.get('dig'),
                nome=request.POST.get('nome'),
                nome_de_guerra=request.POST.get('nome_de_guerra'),
                genero=request.POST.get('genero'),
                nasc=request.POST.get('nasc'),
                matricula=request.POST.get('matricula'),
                admissao=request.POST.get('admissao'),
                previsao_de_inatividade=request.POST.get('previsao_de_inatividade'),
                cpf=cpf,
                rg=request.POST.get('rg'),
                tempo_para_averbar_inss=request.POST.get('tempo_para_averbar_inss'),
                tempo_para_averbar_militar=request.POST.get('tempo_para_averbar_militar'),
                email=request.POST.get('email_funcional'),
                telefone=request.POST.get('telefone'),
                alteracao=request.POST.get('alteracao'),
                user=request.user
            )
            try:
                cadastro.save()
                print("Cadastro salvo com sucesso")

                if request.FILES.get('image'):
                    imagem = Imagem(
                        cadastro=cadastro,
                        image=request.FILES.get('image'),
                        user=request.user
                    )
                    imagem.save()
                    print("Imagem salva com sucesso")

                detalhes = DetalhesSituacao(
                    cadastro=cadastro,
                    situacao=request.POST.get('situacao'),
                    cat_efetivo=request.POST.get('cat_efetivo'),
                    sgb=request.POST.get('sgb'),
                    posto_secao=request.POST.get('posto_secao'),
                    esta_adido=request.POST.get('esta_adido'),
                    funcao=request.POST.get('funcao'),
                    op_adm=request.POST.get('op_adm'),
                    apresentacao_na_unidade=request.POST.get('apresentacao_na_unidade'),
                    saida_da_unidade=request.POST.get('saida_da_unidade'),
                    usuario_alteracao=request.user
                )
                detalhes.save()
                print("Detalhes da situação salvos com sucesso")

                promocao = Promocao(
                    cadastro=cadastro,
                    posto_grad=request.POST.get('posto_grad'),
                    quadro=request.POST.get('quadro'),
                    grupo=request.POST.get('grupo'),
                    ultima_promocao=request.POST.get('ultima_promocao'),
                    usuario_alteracao=request.user
                )
                promocao.save()
                print("Promoção salva com sucesso")

                messages.add_message(request, constants.SUCCESS, 'Militar cadastrado com sucesso')
                return redirect('/efetivo/cadastrar_militar')

            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    messages.add_message(request, constants.ERROR, 'Erro: CPF já cadastrado.')
                else:
                    messages.add_message(request, constants.ERROR, 'Erro ao cadastrar militar. Por favor, tente novamente.')
                return redirect('/efetivo/cadastrar_militar')

        except Exception as e:
            print(f"Erro ao salvar os dados: {e}")
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar militar. Por favor, tente novamente.')
            return redirect('/efetivo/cadastrar_militar')
    


# responsável por listar todos cadastros de militares
def listar_militar(request):
    if request.method == "GET":
      # Subconsulta para obter o último posto_grad de cada Cadastro
        latest_promocao = Promocao.objects.filter(cadastro=OuterRef('pk')).order_by('-ultima_promocao')
        cadastros = Cadastro.objects.annotate(
            latest_posto_grad=Subquery(latest_promocao.values('posto_grad')[:1])
        ).order_by('latest_posto_grad')
        
        return render(request, 'listar_militar.html', {
            'cadastros': cadastros
        })
    
# responsável pelo detalhamento de cada ID de militares
def ver_militar(request, id):
    if id is None:
        messages.add_message(request, constants.ERROR, 'ID inválido')
        return redirect('/efetivo/listar_militar')

    try:
        cadastro = Cadastro.objects.get(id=id)
    except Cadastro.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Militar não encontrado')
        return redirect('/efetivo/listar_militar')

    if request.method == "GET":
        detalhes = DetalhesSituacao.objects.filter(cadastro=cadastro).last()
        promocao = Promocao.objects.filter(cadastro=cadastro).last()
        return render(request, 'ver_militar.html', {
            'cadastro': cadastro,
            'detalhes': detalhes,
            'promocao': promocao,
            'situacao': DetalhesSituacao.situacao_choices,
            'sgb': DetalhesSituacao.sgb_choices,
            'posto_secao': DetalhesSituacao.posto_secao_choices,
            'esta_adido': DetalhesSituacao.esta_adido_choices,
            'funcao': DetalhesSituacao.funcao_choices,
            'op_adm': DetalhesSituacao.op_adm_choices,
            'posto_grad': Promocao.posto_grad_choices,
            'quadro': Promocao.quadro_choices,
            'grupo': Promocao.grupo_choices,
            'genero': Cadastro.genero_choices,
            'cat_efetivo': DetalhesSituacao.cat_efetivo_choices,
        })

# responsável por fazer a exclusão dos cadastros
def excluir_militar(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)
    cadastro.delete()
    messages.add_message(request, constants.SUCCESS, 'Militar deletado com sucesso')
    return redirect('/efetivo/listar_militar')


# responsável pela edição da model promoções
def editar_posto_graduacao(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)
    promocao_atual = cadastro.promocoes.last()

    if request.method == "GET":
        return render(request, 'editar_posto_graduacao.html', {
            'cadastro': cadastro,
            'promocao': promocao_atual,
            'posto_grad': Promocao.posto_grad_choices,
            'quadro': Promocao.quadro_choices,
            'grupo': Promocao.grupo_choices,
        })

    elif request.method == "POST":
        ultima_promocao = request.POST.get('ultima_promocao')
        posto_grad = request.POST.get('posto_grad')
        quadro = request.POST.get('quadro')
        grupo = request.POST.get('grupo')

        if not ultima_promocao:
            messages.add_message(request, constants.ERROR, 'A data da última promoção é obrigatória.')
            return redirect('editar_posto_graduacao', id=cadastro.id)

        if promocao_atual:
            HistoricoPromocao.objects.create(
                cadastro=cadastro,
                posto_grad=promocao_atual.posto_grad,
                quadro=promocao_atual.quadro,
                grupo=promocao_atual.grupo,
                ultima_promocao=promocao_atual.ultima_promocao,
                usuario_alteracao=request.user,
                data_alteracao=timezone.now()
            )

        nova_promocao = Promocao(
            cadastro=cadastro,
            posto_grad=posto_grad,
            quadro=quadro,
            grupo=grupo,
            ultima_promocao=ultima_promocao,
            usuario_alteracao=request.user
        )
        nova_promocao.save()
        messages.add_message(request, constants.SUCCESS,'Dados de Posto e Graduação atualizados com sucesso.')
        return redirect('ver_militar', id=cadastro.id)
    


# responsável pela edição da model pDetalhesSituação
def editar_situacao_atual(request, id):
    if request.method == 'POST':
        cadastro = get_object_or_404(Cadastro, id=id)
        
        try:
            # Log dos dados recebidos
            print("Dados recebidos no POST:", request.POST)
            
            # Atualizar apenas os campos necessários
            detalhes = cadastro.detalhes_situacao.last()
            if detalhes:
                detalhes.situacao = request.POST['situacao_atual']
                detalhes.saida_da_unidade = request.POST.get('saida_da_unidade', None)
                detalhes.save()
            
            messages.add_message(request, constants.SUCCESS, 'Situação atualizada com sucesso.')
            return redirect('listar_militar')  # Substitua pelo nome correto da view

        except Exception as e:
            print(f"Erro ao salvar a situação atual: {e}")
            messages.add_message(request, constants.ERROR, f'Erro ao salvar a situação atual: {e}')
            return redirect('listar_militar')  # Substitua pelo nome correto da view
    
    messages.add_message(request, constants.ERROR, 'Método de requisição inválido.')
    return redirect('listar_militar')  # Substitua pelo nome correto da view



# responsável pelo cadastro de uma nova situação
def cadastrar_nova_situacao(request, id):
    if request.method == 'POST':
        cadastro = get_object_or_404(Cadastro, id=id)
        
        try:
            # Log dos dados recebidos
            print("Dados recebidos no POST:", request.POST)
            
            # Criar Nova Situação
            nova_situacao = DetalhesSituacao(
                cadastro=cadastro,
                situacao=request.POST['situacao'],
                sgb=request.POST['sgb'],
                posto_secao=request.POST['posto_secao'],
                esta_adido=request.POST['esta_adido'],
                funcao=request.POST['funcao'],
                op_adm=request.POST['op_adm'],
                apresentacao_na_unidade=request.POST['apresentacao_na_unidade'],
                saida_da_unidade=request.POST.get('saida_da_unidade', None),
                usuario_alteracao=request.user
            )
            nova_situacao.save()
            
            # Atualizar o Histórico de Detalhes da Situação
            HistoricoDetalhesSituacao.objects.create(
                cadastro=cadastro,
                situacao=nova_situacao.situacao,
                sgb=nova_situacao.sgb,
                posto_secao=nova_situacao.posto_secao,
                esta_adido=nova_situacao.esta_adido,
                funcao=nova_situacao.funcao,
                op_adm=nova_situacao.op_adm,
                apresentacao_na_unidade=nova_situacao.apresentacao_na_unidade,
                saida_da_unidade=nova_situacao.saida_da_unidade,
                data_alteracao=nova_situacao.data_alteracao,
                usuario_alteracao=request.user
            )
            messages.add_message(request, constants.SUCCESS, 'Nova situação criada com sucesso.')
            return redirect('listar_militar')  # Substitua pelo nome correto da view

        except Exception as e:
            print(f"Erro ao cadastrar a nova situação: {e}")
            messages.add_message(request, constants.ERROR, f'Erro ao cadastrar a nova situação: {e}')
            return redirect('listar_militar')  # Substitua pelo nome correto da view
    
    messages.add_message(request, constants.ERROR, 'Método de requisição inválido.')
    return redirect('listar_militar')  # Substitua pelo nome correto da view




# responsável pela edição da model cadastro
def editar_dados_pessoais_contatos(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)
    historico_promocoes = HistoricoPromocao.objects.filter(cadastro=cadastro).order_by('-data_alteracao')
    historico_detalhes_situacao = HistoricoDetalhesSituacao.objects.filter(cadastro=cadastro).order_by('-data_alteracao')

    if request.method == "GET":
        return render(request, 'editar_dados_pessoais_contatos.html', {
            'cadastro': cadastro,
            'genero': Cadastro.genero_choices,
            'historico_promocoes': historico_promocoes,
            'historico_detalhes_situacao': historico_detalhes_situacao,
        })

    elif request.method == "POST":
        cadastro.re = request.POST.get('re')
        cadastro.dig = request.POST.get('dig')
        cadastro.nome = request.POST.get('nome')
        cadastro.nome_de_guerra = request.POST.get('nome_de_guerra')
        cadastro.genero = request.POST.get('genero')
        cadastro.nasc = request.POST.get('nasc')
        cadastro.matricula = request.POST.get('matricula')
        cadastro.admissao = request.POST.get('admissao')
        cadastro.previsao_de_inatividade = request.POST.get('previsao_de_inatividade')
        cadastro.cpf = request.POST.get('cpf')
        cadastro.rg = request.POST.get('rg')
        cadastro.tempo_para_averbar_inss = request.POST.get('tempo_para_averbar_inss')
        cadastro.tempo_para_averbar_militar = request.POST.get('tempo_para_averbar_militar')
        cadastro.email = request.POST.get('email_funcional')
        cadastro.telefone = request.POST.get('telefone')
      
        cadastro.save()
        
        messages.add_message(request, constants.SUCCESS, 'Dados Pessoais e Contatos atualizados com sucesso')
        return redirect('/efetivo/listar_militar')
    

# responsável pela edição da model promoções
def editar_imagem(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)

    if request.method == "POST":
        if request.FILES.get('image'):
            nova_imagem = Imagem(
                cadastro=cadastro,
                image=request.FILES.get('image'),
                user=request.user
            )
            nova_imagem.save()
            messages.add_message(request, constants.SUCCESS, 'Imagem atualizada com sucesso')
        else:
            messages.add_message(request, constants.ERROR, 'Por favor, envie uma imagem válida.')

        return redirect('ver_militar', id=cadastro.id)

    return render(request, 'editar_imagem.html', {
        'cadastro': cadastro,
        'imagem': cadastro.imagens.last()
    })


# responsável por armazenar os dados de movimentação
def historico_movimentacoes(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)
    promocoes = Promocao.objects.filter(cadastro=cadastro).order_by('-data_alteracao')
    historico_detalhes_situacao = HistoricoDetalhesSituacao.objects.filter(cadastro=cadastro).order_by('-data_alteracao')

    return render(request, 'historico_movimentacoes.html', {
        'cadastro': cadastro,
        'promocoes': promocoes,
        'historico_detalhes_situacao': historico_detalhes_situacao,
    })


# responsável pela edição da model De
def editar_situacao_funcional(request, id):
    cadastro = get_object_or_404(Cadastro, id=id)
    
    if request.method == 'POST':
        try:
            # Atualizar a Situação Atual
            cadastro.situacao = request.POST['situacao_atual']
            cadastro.save()
            
            # Criar Nova Situação
            nova_situacao = DetalhesSituacao(
                cadastro=cadastro,
                situacao=request.POST['situacao'],
                sgb=request.POST['sgb'],
                posto_secao=request.POST['posto_secao'],
                esta_adido=request.POST['esta_adido'],
                funcao=request.POST['funcao'],
                op_adm=request.POST['op_adm'],
                apresentacao_na_unidade=request.POST['apresentacao_na_unidade'],
                saida_da_unidade=request.POST.get('saida_da_unidade', None)
            )
            nova_situacao.save()
            
            # Atualizar o Histórico de Detalhes da Situação
            HistoricoDetalhesSituacao.objects.create(
                cadastro=cadastro,
                situacao=nova_situacao.situacao,
                sgb=nova_situacao.sgb,
                posto_secao=nova_situacao.posto_secao,
                esta_adido=nova_situacao.esta_adido,
                funcao=nova_situacao.funcao,
                op_adm=nova_situacao.op_adm,
                apresentacao_na_unidade=nova_situacao.apresentacao_na_unidade,
                saida_da_unidade=nova_situacao.saida_da_unidade,
                data_alteracao=nova_situacao.data_alteracao,
                usuario_alteracao=request.user
            )
            messages.add_message(request, constants.SUCCESS,'Situação funcional atualizada com sucesso!')

        except Exception as e:
            messages.add_message(request, constants.SUCCESS,'Dados de Posto e Graduação atualizados com sucesso.')
            messages.error(request, f'Ocorreu um erro ao atualizar a situação funcional: {e}')
        
        # Permanecer na mesma URL após salvar
        return redirect('editar_situacao_funcional', id=id)
    
    # Renderizar o formulário de edição com os dados atuais
    return render(request, 'editar_situacao_funcional.html', {
        'cadastro': cadastro,
        'situacao': DetalhesSituacao.objects.all(),
        'sgb_choices': DetalhesSituacao._meta.get_field('sgb').choices,
        'posto_secao_choices': DetalhesSituacao._meta.get_field('posto_secao').choices,
        'esta_adido_choices': DetalhesSituacao._meta.get_field('esta_adido').choices,
        'funcao_choices': DetalhesSituacao._meta.get_field('funcao').choices,
        'op_adm_choices': DetalhesSituacao._meta.get_field('op_adm').choices,
        'detalhes': cadastro.detalhes_situacao.last()
    })
from django.shortcuts import render, get_object_or_404, redirect
from backend.documentos.models import Documento,Arquivo
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime
from backend.documentos.forms import DocumentoForm
import logging
logger = logging.getLogger(__name__)


def listar_documentos(request):
    documentos = Documento.objects.all()
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    tipo_selecionado = request.GET.get('tipo')

    if data_inicio:
        documentos = documentos.filter(data_documento__gte=data_inicio)  # Remova __date

    if data_fim:
        documentos = documentos.filter(data_documento__lte=data_fim)  # Remova __date

    if tipo_selecionado:
        documentos = documentos.filter(tipo=tipo_selecionado)

    tipos = Documento.TIPO_CHOICES  # Assumindo que você tem um choices chamado TIPO_CHOICES no seu modelo

    context = {
        'documentos': documentos,
        'data_inicio': data_inicio.strftime('%Y-%m-%d') if data_inicio else None,
        'data_fim': data_fim.strftime('%Y-%m-%d') if data_fim else None,
        'tipo_selecionado': tipo_selecionado,
        'tipos': tipos,
    }

    return render(request, 'listar_documentos.html', context) # Substitua 'seu_template.html' pelo nome do seu template

from django.shortcuts import render, get_object_or_404, redirect
from backend.documentos.models import Documento
from django.http import HttpResponse
import markdown  # Importe a biblioteca markdown

# views.py (atualização da view detalhe_documento)

def detalhe_documento(request, pk):
    documento = get_object_or_404(
        Documento.objects.prefetch_related('arquivos'),  # ← Otimiza o carregamento
        pk=pk
    )
    
    # Processar descrição Markdown
    import markdown
    descricao_html = markdown.markdown(documento.descricao)
    
    return render(request, 'detalhe_documento.html', {
        'documento': documento,
        'arquivos': documento.arquivos.all(),  # ← Garante o relacionamento
        'descricao_html': descricao_html
    })





def criar_documento(request):
    tipos = Documento.TIPO_CHOICES

    if request.method == 'POST':
        try:
            data_publicacao = request.POST.get('data_publicacao')
            data_documento = request.POST.get('data_documento')
            numero_documento = request.POST.get('numero_documento')
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')
            assinada_por = request.POST.get('assinada_por')
            arquivos = request.FILES.getlist('arquivos[]')
            tipo = request.POST.get('tipo')
            tipos_arquivos = request.POST.getlist('tipo[]')

            # Parse datetime strings to datetime objects
            data_publicacao = parse_datetime(data_publicacao)
            data_documento = parse_datetime(data_documento)

            if not all([data_publicacao, data_documento, numero_documento, assunto]):
                return render(request, 'criar_documento.html', {
                    'error': 'Campos obrigatórios faltando',
                    'tipos': tipos
                })

            documento = Documento(
                data_publicacao=data_publicacao,
                data_documento=data_documento,
                numero_documento=numero_documento,
                assunto=assunto,
                descricao=descricao,
                assinada_por=assinada_por,
                tipo=tipo,
                usuario=request.user
            )
            documento.save()

            if len(arquivos) != len(tipos_arquivos):
                raise ValueError("Número de arquivos e tipos não corresponde")

            for arquivo, tipo in zip(arquivos, tipos_arquivos):
                Arquivo.objects.create(
                    documento=documento,
                    arquivo=arquivo,
                    tipo=tipo
                )

            return redirect('documentos:listar_documentos')

        except Exception as e:
            return render(request, 'criar_documento.html', {
                'error': str(e),
                'tipos': tipos
            })

    return render(request, 'criar_documento.html', {'tipos': tipos})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Documento, Arquivo
from .forms import DocumentoForm
import logging

logger = logging.getLogger(__name__)

def editar_documento(request, pk):
    documento = get_object_or_404(Documento.objects.prefetch_related('arquivos'), pk=pk)
    tipos = Documento.TIPO_CHOICES

    if request.method == 'POST':
        form = DocumentoForm(request.POST, instance=documento)
        if form.is_valid():
            try:
                documento = form.save(commit=False)
                if request.user.is_authenticated:
                    documento.usuario = request.user
                else:
                    messages.error(request, "Usuário não autenticado.")
                    return redirect('login')
                documento.save()
                messages.success(request, 'Documento atualizado com sucesso!')
                return redirect('documentos:detalhe_documento', pk=pk)
            except Exception as e:
                logger.error(f"Erro ao salvar documento: {e}")
                messages.error(request, 'Erro ao salvar documento. Tente novamente.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    form = DocumentoForm(instance=documento)

    return render(request, 'editar_documento.html', {
        'documento': documento,
        'form': form,
    })

def editar_documento_arquivos(request, pk):
    documento = get_object_or_404(Documento.objects.prefetch_related('arquivos'), pk=pk)
    tipos = Documento.TIPO_CHOICES

    if request.method == 'POST':
        novos_arquivos = request.FILES.getlist('novos_arquivos')
        novos_tipos = request.POST.getlist('novos_tipos')

        # Validação aprimorada
        validos = []
        for arquivo, tipo in zip(novos_arquivos, novos_tipos):
            if arquivo.size > 0 and tipo in dict(tipos).keys():
                validos.append((arquivo, tipo))

        if len(validos) > 0:
            for arquivo, tipo in validos:
                Arquivo.objects.create(
                    documento=documento, 
                    arquivo=arquivo, 
                    tipo=tipo
                )
            messages.success(request, 'Arquivos atualizados com sucesso!')
        else:
            messages.error(request, 'Nenhum arquivo válido para upload')

        return redirect('documentos:editar_documento_arquivos', pk=pk)

    return render(request, 'editar_documento_arquivos.html', {
        'documento': documento, 
        'tipos': tipos
    })



def excluir_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        documento.delete()
        return redirect('documentos:listar_documentos')
    return render(request, 'listar_documentos.html', {'documento': documento})

def carrossel_noticias(request):
    ultimas_noticias = Documento.objects.order_by('-data_criacao')[:5]
    return render(request, 'carrossel_noticias.html', {'ultimas_noticias': ultimas_noticias})

def carregar_conteudo_arquivo(request, pk):
    arquivo = get_object_or_404(Arquivo, pk=pk)
    if arquivo.tipo == 'TEXT' or arquivo.tipo == 'DOC':
        try:
            with arquivo.arquivo.open('r') as f:
                conteudo = f.read()
            return HttpResponse(conteudo, content_type='text/plain')
        except Exception as e:
            return HttpResponse(f"Erro ao ler arquivo: {str(e)}", status=500)
    elif arquivo.tipo == 'PDF': # adicionado para pdf
          return HttpResponse(arquivo.arquivo, content_type='application/pdf')

    else:
        return HttpResponse("Tipo de arquivo não suportado para visualização de conteúdo.", status=400)





from django.http import JsonResponse

def excluir_arquivo(request, arquivo_id):
    if request.method == 'POST':
         arquivo = get_object_or_404(Arquivo, pk=arquivo_id)
         try:
            arquivo.delete()
            return JsonResponse({'status': 'success'})
         except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)





from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages



def gerenciar_arquivos(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    tipos = Arquivo.TIPO_CHOICES  
    
    if request.method == 'POST':
        try:
            # Processar arquivos existentes
            for key, value in request.POST.items():
                if key.startswith('tipo_'):
                    arquivo_id = key.split('_')[1]
                    arquivo = Arquivo.objects.get(id=arquivo_id)
                    arquivo.tipo = value
                    arquivo.save()

            # Processar novos arquivos
            novos_arquivos = request.FILES.getlist('novos_arquivos')
            novos_tipos = request.POST.getlist('novos_tipos')
            
            for arquivo, tipo in zip(novos_arquivos, novos_tipos):
                Arquivo.objects.create(
                    documento=documento,
                    arquivo=arquivo,
                    tipo=tipo
                )

            messages.success(request, 'Alterações salvas com sucesso!')
        except Exception as e:
            messages.error(request, f'Erro ao salvar alterações: {str(e)}')

        return redirect('documentos:detalhe_documento', pk=pk)

    return redirect('documentos:listar_documentos')
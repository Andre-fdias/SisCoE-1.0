from django.shortcuts import render, get_object_or_404, redirect
from backend.documentos.models import Documento,Arquivo
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime

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
    if request.method == 'POST':
        data_publicacao = request.POST['data_publicacao']
        data_documento = request.POST['data_documento']
        numero_documento = request.POST['numero_documento']
        assunto = request.POST['assunto']
        descricao = request.POST['descricao']
        assinada_por = request.POST['assinada_por']
        arquivos = request.FILES.getlist('arquivos[]')
        tipos = request.POST.getlist('tipo[]')

        # Crie um novo objeto Documento e salve no banco de dados
        documento = Documento(
            data_publicacao=data_publicacao,
            data_documento=data_documento,
            numero_documento=numero_documento,
            assunto=assunto,
            descricao=descricao,
            assinada_por=assinada_por,
            usuario=request.user  # Assumindo que o usuário está logado
        )
        documento.save()

        # Verifique se o número de arquivos e tipos corresponde
        if len(arquivos) == len(tipos):
            for i in range(len(arquivos)):
                arquivo = arquivos[i]
                tipo = tipos[i]

                # Crie um novo objeto Arquivo e associe ao documento
                Arquivo.objects.create(
                    documento=documento,
                    arquivo=arquivo,
                    tipo=tipo
                )

            return redirect('documentos:listar_documentos')  # Redirecione para a lista de documentos

        else:
            # Lidar com o erro de número incorreto de arquivos/tipos
            return render(request, 'criar_documento.html', {'error': 'Número de arquivos e tipos não corresponde.'})

    return render(request, 'criar_documento.html')


# views.py (atualizar a view editar_documento)
from django.forms import modelform_factory

def editar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk)
    DocumentoForm = modelform_factory(Documento, fields='__all__')
    
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            documento = form.save()
            
            # Processar novos arquivos
            novos_arquivos = request.FILES.getlist('novos_arquivos')
            for arquivo in novos_arquivos:
                Arquivo.objects.create(
                    documento=documento,
                    arquivo=arquivo,
                    tipo=documento.tipo
                )
            
            return redirect('documentos:detalhe_documento', pk=pk)
    else:
        form = DocumentoForm(instance=documento)
    
    return render(request, 'editar_documento.html', {
        'documento': documento,
        'form': form
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

    # views.py
def remover_arquivo(request, pk):
    arquivo = get_object_or_404(Arquivo, pk=pk)
    if request.method == 'POST':
        arquivo.delete()
    return redirect('documentos:detalhe_documento', pk=arquivo.documento.pk)
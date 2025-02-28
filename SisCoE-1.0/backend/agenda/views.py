from django.shortcuts import render, get_object_or_404, redirect
from .models import Lembrete, Tarefa
from .forms import LembreteForm, TarefaForm

def calendario(request):
    user = request.user
    lembretes = Lembrete.objects.filter(user=user) | Lembrete.objects.filter(visibilidade='publico')
    tarefas = Tarefa.objects.filter(user=user) | Tarefa.objects.filter(visibilidade='publico')
    lembrete_form = LembreteForm()
    tarefa_form = TarefaForm()
    return render(request, 'calendario.html', {
        'lembretes': lembretes,
        'tarefas': tarefas,
        'lembrete_form': lembrete_form,
        'tarefa_form': tarefa_form
    })

def lembrete_novo(request):
    if request.method == "POST":
        form = LembreteForm(request.POST)
        if form.is_valid():
            lembrete = form.save(commit=False)
            lembrete.user = request.user
            lembrete.save()
            return redirect('agenda:calendario')
    return redirect('agenda:calendario')

def tarefa_nova(request):
    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa = form.save(commit=False)
            tarefa.user = request.user
            tarefa.save()
            return redirect('agenda:calendario')
    return redirect('agenda:calendario')

def lembrete_editar(request, pk):
    lembrete = get_object_or_404(Lembrete, pk=pk)
    if request.method == "POST":
        form = LembreteForm(request.POST, instance=lembrete)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = LembreteForm(instance=lembrete)
    return render(request, 'lembrete_form.html', {'form': form})

def lembrete_deletar(request, pk):
    lembrete = get_object_or_404(Lembrete, pk=pk)
    if request.method == "POST":
        lembrete.delete()
        return redirect('calendario')
    return render(request, 'eventos/lembrete_confirm_delete.html', {'lembrete': lembrete})

def tarefa_editar(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'eventos/tarefa_form.html', {'form': form})

def tarefa_deletar(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)
    if request.method == "POST":
        tarefa.delete()
        return redirect('calendario')
    return render(request, 'eventos/tarefa_confirm_delete.html', {'tarefa': tarefa})

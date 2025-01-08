from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def capa(request):
    template_name = 'landing.html'
    return render(request, template_name)


@login_required
def index(request):
    template_name = 'index.html'
    return render(request, template_name)


@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)




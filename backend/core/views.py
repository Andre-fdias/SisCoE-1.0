from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from backend.efetivo.models import Cadastro


def capa(request):
    template_name = 'landing.html'
    return render(request, template_name)




@login_required

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)


@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profiles/profile.html', {'profile': profile})


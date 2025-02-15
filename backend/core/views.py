from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from .models import Profile


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



@login_required
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request, 'accounts/user_list.html', {'profiles': profiles})



@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'accounts/accounts/user_detail.html', {'profile': profile})



@login_required
def profile_create(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        cadastro = request.POST.get('cadastro')
        re = request.POST.get('re')
        dig = request.POST.get('dig')
        posto_grad = request.POST.get('posto_grad')
        image = request.FILES.get('image')
        cpf = request.POST.get('cpf')
        tipo = request.POST.get('tipo')
        
        profile = Profile(user=user, cadastro=cadastro, re=re, dig=dig, posto_grad=posto_grad, image=image, cpf=cpf, tipo=tipo)
        profile.save()
        return redirect('core:profile_list')
    return render(request, 'profiles/profile_form.html')

@login_required
def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posto_grad_choices = Profile.posto_grad_choices
    tipo_choices = Profile.tipo_choices

    if request.method == 'POST':
        profile.cpf = request.POST.get('cpf')
        profile.posto_grad = request.POST.get('posto_grad')
        profile.re = request.POST.get('re')
        profile.dig = request.POST.get('dig')
        profile.tipo = request.POST.get('tipo')
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        
        profile.save()
        return redirect('core:profile_detail', pk=pk)
    
    context = {
        'profile': profile,
        'posto_grad_choices': posto_grad_choices,
        'tipo_choices': tipo_choices,
    }
    return render(request, 'profiles/profile_form.html', context)

@login_required
def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return redirect('core:profile_list')
    return render(request, 'profiles/profile_confirm_delete.html', {'profile': profile})

 #accounts/views.py
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import get_user_model

from backend.accounts.services import send_mail_to_user
from .forms import CustomUserForm
from .models import AuditEntry, User
from .services import send_mail_to_user_reset_password
from .signals import user_login_password_failed

from backend.efetivo.models import Cadastro, DetalhesSituacao, Promocao, Imagem  # Ajuste a importaÃ§Ã£o conforme necessÃ¡rio
from django.contrib.auth.decorators import login_required




def my_logout(request):
    # ... logout logic
    return redirect('core:capa')



def signup(request):
    '''
    Cadastra Usuário.
    '''
    template_name = 'registration/registration_form.html'
    form = CustomUserForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            send_mail_to_user(request=request, user=user)
            return redirect('login')

    return render(request, template_name)


class MyPasswordResetConfirm(PasswordResetConfirmView):
    '''
    Requer password_reset_confirm.html
    '''

    def form_valid(self, form):
        self.user.is_active = True
        self.user.save()
        return super(MyPasswordResetConfirm, self).form_valid(form)


class MyPasswordResetComplete(PasswordResetCompleteView):
    '''
    Requer password_reset_complete.html
    '''
    ...


class MyPasswordReset(PasswordResetView):
    '''
    Requer
    registration/password_reset_form.html
    registration/password_reset_email.html
    registration/password_reset_subject.txt  Opcional
    '''
    ...


class MyPasswordResetDone(PasswordResetDoneView):
    '''
    Requer
    registration/password_reset_done.html
    '''
    ...

User = get_user_model()

def verificar_cpf(request):
    '''
    Verifica se o CPF está cadastrado e se o usuário é ativo.
    '''
    template_name = 'registration/verificacao_cpf.html'
    message = None

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            # Verifica se o CPF está cadastrado na model Cadastro
            cadastro = Cadastro.objects.get(cpf=cpf)
            print(f"Cadastro encontrado: {cadastro}")
            
            # Verifica se o usuário é ativo na model DetalhesSituacao
            detalhes_situacao = DetalhesSituacao.objects.get(cadastro=cadastro)
            print(f"Detalhes da situação encontrados: {detalhes_situacao}")
            print(f"Situação: {detalhes_situacao.situacao}")
            
            if detalhes_situacao.situacao == 'ATIVO':
                # Verifica se o usuário já está cadastrado na model User
                if User.objects.filter(email=cadastro.email).exists():
                    message = 'Usuário já cadastrado. Por favor, faça login.'
                else:
                    print("Redirecionando para a página de cadastro...")
                    return redirect('signup')  # Redireciona para a página de cadastro
            else:
                message = 'Você não é um funcionário ativo. Por favor, procure o setor de RH.'
        except Cadastro.DoesNotExist:
            message = 'CPF não encontrado. Por favor, procure o setor de RH.'
        except DetalhesSituacao.DoesNotExist:
            message = 'Detalhes da situação não encontrados. Por favor, procure o setor de RH.'
        except Exception as e:
            message = f"Ocorreu um erro: {e}"
            print(f"Erro: {e}")

    return render(request, template_name, {'message': message})




def user_list(request):
    template_name = 'accounts/user_list.html'
    object_list = User.objects.exclude(email='admin@email.com')
    context = {'object_list': object_list}
    return render(request, template_name, context)


def user_detail(request, pk):
    template_name = 'accounts/user_detail.html'
    instance = get_object_or_404(User, pk=pk)

    context = {'object': instance}
    return render(request, template_name, context)


def user_create(request):
    template_name = 'accounts/user_form.html'
    form = CustomUserForm(request.POST or None)

    context = {'form': form}
    return render(request, template_name, context)


def user_update(request, pk):
    template_name = 'accounts/user_form.html'
    instance = get_object_or_404(User, pk=pk)
    form = CustomUserForm(request.POST or None, instance=instance)

    context = {
        'object': instance,
        'form': form,
    }
    return render(request, template_name, context)




@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profiles/profile.html', {'profile': profile})



@login_required
def edit_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/profile_form.html', {'form': form})


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = user.profile
    return render(request, 'accounts/user_detail.html', {'object': user, 'profile': profile})
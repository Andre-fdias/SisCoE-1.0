# accounts/views.py
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from backend.accounts.services import send_mail_to_user
from backend.efetivo.models import Cadastro, DetalhesSituacao, Promocao, Imagem  # Ajuste a importaÃ§Ã£o conforme necessÃ¡rio
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
import socket
from .models import User
from .forms import CustomUserForm
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from datetime import datetime
from django.utils.timezone import make_naive, is_aware



def my_logout(request):
    user = request.user
    user.update_login_history(None, None, logout_time=timezone.now())
    user.is_online = False
    user.save()
    logout(request)
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



@login_required
def user_list(request):
    template_name = 'accounts/user_list.html'
    object_list = User.objects.exclude(email='admin@email.com')
    context = {'object_list': object_list}
    return render(request, template_name, context)

@login_required
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


@login_required
def user_update(request, pk):
    template_name = 'accounts/user_form.html'
    instance = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)  # Redireciona para a página de detalhes do usuário após a atualização
    else:
        form = CustomUserForm(instance=instance)

    context = {
        'object': instance,
        'form': form,
    }
    return render(request, template_name, context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_computer_name(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return 'Unknown'
    

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            user_ip = get_client_ip(request)
            user_computer_name = get_computer_name(user_ip)
            user.update_login_history(user_ip, user_computer_name, login_time=timezone.now())
            user.is_online = True
            user.save()
            login(request, user)
            return redirect('core:index')
    return render(request, 'registration/login.html', {'form': form})


@login_required
def access_history(request):
    user = request.user
    login_history = []
    for entry in user.login_history:
        login_time = entry.get('login_time')
        logout_time = entry.get('logout_time')
        duration = user.get_login_duration(login_time, logout_time)
        formatted_login_time = user.format_datetime(login_time)
        formatted_logout_time = user.format_datetime(logout_time)
        login_history.append({
            'login_time': formatted_login_time,
            'ip': entry.get('ip'),
            'computer_name': entry.get('computer_name'),
            'logout_time': formatted_logout_time,
            'duration': duration,
            'is_online': user.is_online,
        })
    return render(request, 'accounts/access_history.html', {'login_history': login_history})



@login_required
def all_users_list(request):
    users = User.objects.all()
    selected_user = request.GET.get('user')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    all_login_history = []
    for user in users:
        if selected_user and user.email != selected_user:
            continue
        for entry in user.login_history:
            login_time = entry.get('login_time')
            logout_time = entry.get('logout_time')
            
            # Convert to naive datetime if aware
            if login_time and is_aware(datetime.fromisoformat(login_time)):
                login_time = make_naive(datetime.fromisoformat(login_time))
            if logout_time and is_aware(datetime.fromisoformat(logout_time)):
                logout_time = make_naive(datetime.fromisoformat(logout_time))
            
            if start_date and login_time:
                if datetime.fromisoformat(start_date) > login_time:
                    continue
            if end_date and logout_time:
                if datetime.fromisoformat(end_date) < logout_time:
                    continue
            duration = user.get_login_duration(login_time.isoformat() if login_time else None, logout_time.isoformat() if logout_time else None)
            formatted_login_time = user.format_datetime(login_time.isoformat() if login_time else None)
            formatted_logout_time = user.format_datetime(logout_time.isoformat() if logout_time else None)
            all_login_history.append({
                'email': user.email,
                'login_time': formatted_login_time,
                'ip': entry.get('ip'),
                'computer_name': entry.get('computer_name'),
                'logout_time': formatted_logout_time,
                'duration': duration,
                'is_online': user.is_online,
            })
    return render(request, 'accounts/all_list.html', {
        'all_login_history': all_login_history,
        'users': users,
        'selected_user': selected_user,
        'start_date': start_date,
        'end_date': end_date,
    })
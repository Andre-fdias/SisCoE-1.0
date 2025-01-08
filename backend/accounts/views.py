# accounts/views.py
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    LoginView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView
)
from django.shortcuts import redirect, render

from backend.accounts.services import send_mail_to_user
from backend.efetivo.models import Cadastro, DetalhesSituacao, Promocao, Imagem  # Ajuste a importaÃ§Ã£o conforme necessÃ¡rio

from .forms import CustomUserForm


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

def verificar_cpf(request):
    '''
    Verifica se o CPF está cadastrado e se o usuário é ativo.
    '''
    template_name = 'registration/verificacao_cpf.html'
    message = None

    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        try:
            cadastro = Cadastro.objects.get(cpf=cpf)
            print(f"Cadastro encontrado: {cadastro}")
            detalhes_situacao = DetalhesSituacao.objects.get(cadastro=cadastro)
            print(f"Detalhes da situação encontrados: {detalhes_situacao}")
            print(f"Situação: {detalhes_situacao.situacao}")
            if detalhes_situacao.situacao == 'ATIVO':  # Ajuste aqui para verificar "ATIVO"
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
# accounts/services.py

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from .models import UserActionLog
from .utils import get_client_ip, get_computer_name  # Atualize esta linha

def send_mail_to_user(request, user):
    current_site = get_current_site(request)
    use_https = request.is_secure()
    subject = 'Redefinição de senha'
    message = render_to_string('email/password_reset_email.html', {
        'user': user,
        'protocol': 'https' if use_https else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)

def log_user_action(user, action, request=None):
    ip_address = get_client_ip(request) if request else None
    computer_name = get_computer_name(ip_address) if ip_address else None
    UserActionLog.objects.create(
        user=user,
        action=action,
        ip_address=ip_address,
        computer_name=computer_name
    )


from .models import UserActionLog
from .utils import get_client_ip, get_computer_name

def log_user_action(user, action, request=None):
    ip_address = get_client_ip(request) if request else None
    computer_name = get_computer_name(ip_address) if ip_address else None
    UserActionLog.objects.create(
        user=user,
        action=action,
        ip_address=ip_address,
        computer_name=computer_name
    )
# accounts/models.py
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from backend.core.models import TimeStampedModel

from .managers import UserManager
from .signals import user_login_password_failed

# https://stackoverflow.com/a/37620866/802542


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_absolute_url(self):
        return reverse_lazy('user_detail', kwargs={'pk': self.pk})


@receiver(post_save, sender=User)
def send_email_on_user_creation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Novo usuário criado',
            f'Um novo usuário com email {instance.email} foi criado.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )

from backend.efetivo.models import Cadastro

class Profile(models.Model):
    posto_grad_choices = (
        ("", " "),
        ("Cel PM", "Cel PM"),
        ("Ten Cel PM", "Ten Cel PM"),
        ("Maj PM", "Maj PM"),
        ("CAP PM", "Cap PM"),
        ("1º Ten PM", "1º Ten PM"),
        ("1º Ten QAPM", "1º Ten QAOPM"),
        ("2º Ten PM", "2º Ten PM"),
        ("2º Ten QAPM", "2º Ten QAOPM"),
        ("Asp OF PM", "Asp OF PM"),
        ("Subten PM", "Subten PM"),
        ("1º Sgt PM", "1º Sgt PM"),
        ("2º Sgt PM", "2º Sgt PM"),
        ("3º Sgt PM", "3º Sgt PM"),
        ("Cb PM", "Cb PM"),
        ("Sd PM", "Sd PM"),
        ("Sd PM 2ºCL", "Sd PM 2ºCL"),
    )
    
    tipo_choices = (
        ("administrativo", "Administrativo"),
        ("operacional", "Operacional"),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='usuário'
    )
    cadastro = models.OneToOneField(
        Cadastro,
        on_delete=models.CASCADE,
        verbose_name='cadastro',
        null=True,  # Permitir valores nulos temporariamente
        blank=True
    )
    re = models.CharField(max_length=6, blank=False, null=False, unique=True)
    dig = models.CharField(max_length=1, blank=False, null=False)
    posto_grad = models.CharField(max_length=100, choices=posto_grad_choices)
    image = models.ImageField(upload_to='img/fotos_perfil/usuario')
    cpf = models.CharField(max_length=14, blank=False, null=False, unique=True)
    tipo = models.CharField(max_length=15, choices=tipo_choices, blank=False, null=False)

    class Meta:
        ordering = ('user__first_name',)
        verbose_name = 'perfil'
        verbose_name_plural = 'perfis'

    @property
    def full_name(self):
        return f' {self.user.last_name}'.strip()

    def __str__(self):
        return self.full_name

    @property
    def grad(self):
        if self.posto_grad == 'Cel PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Cel PM</span>')
        if self.posto_grad == 'Ten Cel PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Ten Cel PM</span>')
        if self.posto_grad == 'Maj PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Maj PM</span>')
        if self.posto_grad == 'CAP PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">CAP PM</span>')
        if self.posto_grad == '1º Ten PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">1º Ten PM</span>')
        if self.posto_grad == '1º Ten QAPM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">1º Ten QAPM</span>')
        if self.posto_grad == '2º Ten PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">2º Ten PM</span>')
        if self.posto_grad == '2º Ten QAPM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">2º Ten QAPM</span>')
        if self.posto_grad == 'Asp OF PM':
            return mark_safe('<span class="bg-blue-500 text-white px-2 py-1 rounded">Asp OF PM</span>')
        if self.posto_grad == 'Subten PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">Subten PM</span>')
        if self.posto_grad == '1º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">1º Sgt PM</span>')
        if self.posto_grad == '2º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">2º Sgt PM</span>')
        if self.posto_grad == '3º Sgt PM':
            return mark_safe('<span class="bg-red-500 text-white px-2 py-1 rounded">3º Sgt PM</span>')
        if self.posto_grad == 'Cb PM':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Cb PM</span>')
        if self.posto_grad == 'Sd PM':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Sd PM</span>')
        if self.posto_grad == 'Sd PM 2ºCL':
            return mark_safe('<span class="bg-black text-white px-2 py-1 rounded">Sd PM 2ºCL</span>')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





class AuditEntry(TimeStampedModel):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    email = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return f'{self.action}-{self.email}-{self.ip}'

    def __str__(self):
        return f'{self.action}-{self.email}-{self.ip}'


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_in',
        ip=ip,
        email=user.email
    )


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(
        action='user_logged_out',
        ip=ip,
        email=user.email
    )


@receiver(user_login_password_failed)
def user_login_password_failed(sender, **kwargs):
    user = kwargs['user']
    AuditEntry.objects.create(
        action='user_login_password_failed',
        email=user.email
    )
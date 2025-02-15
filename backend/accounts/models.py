# accounts/models.py
from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import datetime, timedelta

from .managers import UserManager


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
            'Designates whether the user can log into this admin site.'),)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    last_login_computer_name = models.CharField(max_length=255, null=True, blank=True)
    login_history = models.JSONField(default=list, blank=True)
    is_online = models.BooleanField(default=False)


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
    

    
    def update_login_history(self, ip, computer_name, login_time=None, logout_time=None):
        if login_time:
            self.login_history.append({
                'login_time': login_time.isoformat(),
                'ip': ip,
                'computer_name': computer_name,
                'logout_time': None,
            })
        if logout_time:
            self.login_history[-1]['logout_time'] = logout_time.isoformat()
        self.save()


    def get_login_duration(self, login_time, logout_time):
        if login_time and logout_time:
            login_dt = datetime.fromisoformat(login_time)
            logout_dt = datetime.fromisoformat(logout_time)
            duration = logout_dt - login_dt
            total_seconds = int(duration.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{hours:02}:{minutes:02}:{seconds:02}'
        return None

    def format_datetime(self, dt_str):
        if dt_str:
            dt = datetime.fromisoformat(dt_str)
            return dt.strftime('%d/%m/%Y - %H:%M:%S')
        return None
    

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    computer_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.timestamp}"
# accounts/middleware.py

from django.utils.deprecation import MiddlewareMixin
from .services import log_user_action

class UserActionLoggingMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            action = f"Accessed {view_func.__name__} view"
            log_user_action(request.user, action, request)
        return None
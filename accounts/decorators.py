# accounts/decorators.py
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

def admin_cliente_required(function):
    """
    Decorator que verifica se o usuário logado tem o perfil 'ADMIN_CLIENTE'.
    """
    def wrap(request, *args, **kwargs):
        if request.user.tipo_perfil == 'ADMIN_CLIENTE':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def administrador_required(function):
    """
    Decorator que verifica se o usuário logado tem o perfil 'ADMINISTRADOR'.
    """
    def wrap(request, *args, **kwargs):
        if request.user.tipo_perfil == 'ADMINISTRADOR':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

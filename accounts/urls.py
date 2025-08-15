# accounts/urls.py
from django.urls import path
# Importe a LogoutView padrão
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, register_view, dashboard_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registrar/', register_view, name='register'),
    # Aponte a URL de logout para a view padrão do Django
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

# gestao/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.gerenciar_usuarios_view, name='gerenciar_usuarios'),
    path('usuarios/adicionar/', views.adicionar_usuario_view, name='adicionar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario_view, name='editar_usuario'),
]

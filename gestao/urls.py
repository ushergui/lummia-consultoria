# gestao/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs do Admin Cliente
    path('equipe/', views.gerenciar_usuarios_view, name='gerenciar_usuarios'),
    path('equipe/adicionar/', views.adicionar_usuario_view, name='adicionar_usuario'),
    path('equipe/editar/<int:pk>/', views.editar_usuario_view, name='editar_usuario'),

    # URLs do Admin da Plataforma
    path('admin/empresas/', views.gerenciar_empresas_view, name='gerenciar_empresas'),
    path('admin/empresas/nova/', views.criar_empresa_view, name='criar_empresa'),
    path('admin/empresas/editar/<int:pk>/', views.editar_empresa_view, name='editar_empresa'),
    path('admin/usuarios/', views.gerenciar_todos_usuarios_view, name='gerenciar_todos_usuarios'),
    path('admin/usuarios/novo/', views.criar_usuario_plataforma_view, name='criar_usuario_plataforma'),
    path('admin/usuarios/editar/<int:pk>/', views.editar_usuario_plataforma_view, name='editar_usuario_plataforma'),
]

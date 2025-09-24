# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URLs públicas
    path('', views.index, name='index'),
    path('sobre/', views.sobre, name='sobre'),
    path('noticia/<int:pk>/', views.noticia_detalhe_view, name='noticia_detalhe'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('prompts/', views.prompt_library, name='prompt_library'),
    
    # URLs de Gerenciamento de Notícias
    path('gerenciar/noticias/', views.gerenciar_noticias, name='gerenciar_noticias'),
    path('gerenciar/noticias/nova/', views.criar_noticia, name='criar_noticia'),
    path('gerenciar/noticias/editar/<int:pk>/', views.editar_noticia, name='editar_noticia'),
    path('gerenciar/noticias/deletar/<int:pk>/', views.deletar_noticia, name='deletar_noticia'),
]

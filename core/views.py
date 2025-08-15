# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from .forms import NoticiaForm

# --- Views Públicas ---

def index(request):
    """
    View para a página inicial. Agora busca as 3 notícias mais recentes.
    """
    noticias_recentes = Noticia.objects.all()[:3]
    context = {
        'noticias': noticias_recentes
    }
    return render(request, 'index.html', context)

def sobre(request):
    """
    View para a página 'Sobre Nós'.
    """
    context = {}
    return render(request, 'sobre.html', context)

# --- Views de Gerenciamento (CRUD de Notícias) ---

def gerenciar_noticias(request):
    """
    Lista todas as notícias para gerenciamento.
    """
    lista_noticias = Noticia.objects.all()
    context = {
        'noticias': lista_noticias
    }
    return render(request, 'gerenciar_noticias.html', context)

def criar_noticia(request):
    """
    Cria uma nova notícia.
    """
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_noticias')
    else:
        form = NoticiaForm()
    
    context = {
        'form': form,
        'titulo_pagina': 'Adicionar Nova Notícia'
    }
    return render(request, 'noticia_form.html', context)

def editar_noticia(request, pk):
    """
    Edita uma notícia existente.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_noticias')
    else:
        form = NoticiaForm(instance=noticia)
        
    context = {
        'form': form,
        'titulo_pagina': 'Editar Notícia'
    }
    return render(request, 'noticia_form.html', context)

def deletar_noticia(request, pk):
    """
    Deleta uma notícia.
    """
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('gerenciar_noticias')
        
    context = {
        'noticia': noticia
    }
    return render(request, 'noticia_confirm_delete.html', context)

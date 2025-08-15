# core/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # Importe o decorator
from .models import Noticia
from .forms import NoticiaForm

# --- Views Públicas (não precisam de login) ---

def index(request):
    noticias_recentes = Noticia.objects.all()[:3]
    context = {'noticias': noticias_recentes}
    return render(request, 'index.html', context)

def sobre(request):
    context = {}
    return render(request, 'sobre.html', context)

# --- Views de Gerenciamento (AGORA PROTEGIDAS) ---

@login_required
def gerenciar_noticias(request):
    lista_noticias = Noticia.objects.all()
    context = {'noticias': lista_noticias}
    return render(request, 'gerenciar_noticias.html', context)

@login_required
def criar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_noticias')
    else:
        form = NoticiaForm()
    context = {'form': form, 'titulo_pagina': 'Adicionar Nova Notícia'}
    return render(request, 'noticia_form.html', context)

@login_required
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_noticias')
    else:
        form = NoticiaForm(instance=noticia)
    context = {'form': form, 'titulo_pagina': 'Editar Notícia'}
    return render(request, 'noticia_form.html', context)

@login_required
def deletar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('gerenciar_noticias')
    context = {'noticia': noticia}
    return render(request, 'noticia_confirm_delete.html', context)

# core/views.py
from django.shortcuts import render

def index(request):
    """
    View para a página inicial.
    """
    # Futuramente, vamos buscar as notícias do banco de dados aqui.
    context = {}
    return render(request, 'index.html', context)

def sobre(request):
    """
    View para a página 'Sobre Nós'.
    """
    context = {}
    return render(request, 'sobre.html', context)

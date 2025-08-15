# gestao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_cliente_required
from accounts.models import CustomUser
from .forms import AdicionarUsuarioForm, EditarUsuarioForm

@login_required
@admin_cliente_required
def gerenciar_usuarios_view(request):
    """
    Lista todos os usuários da empresa do Admin_Cliente logado.
    """
    # Filtra os usuários que pertencem à mesma empresa do usuário logado
    usuarios_da_empresa = CustomUser.objects.filter(empresa=request.user.empresa)
    context = {
        'usuarios': usuarios_da_empresa
    }
    return render(request, 'gestao/gerenciar_usuarios.html', context)

@login_required
@admin_cliente_required
def adicionar_usuario_view(request):
    if request.method == 'POST':
        form = AdicionarUsuarioForm(request.POST)
        if form.is_valid():
            novo_usuario = form.save(commit=False)
            # Associa o novo usuário à empresa do admin que o está criando
            novo_usuario.empresa = request.user.empresa
            # Define o perfil como Servidor Cliente por padrão
            novo_usuario.tipo_perfil = 'SERVIDOR_CLIENTE'
            novo_usuario.save()
            return redirect('gerenciar_usuarios')
    else:
        form = AdicionarUsuarioForm()
    
    context = {
        'form': form,
        'titulo_pagina': 'Adicionar Novo Usuário à Equipe'
    }
    return render(request, 'gestao/usuario_form.html', context)

@login_required
@admin_cliente_required
def editar_usuario_view(request, pk):
    usuario_para_editar = get_object_or_404(CustomUser, pk=pk, empresa=request.user.empresa)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario_para_editar)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_usuarios')
    else:
        form = EditarUsuarioForm(instance=usuario_para_editar)
    
    context = {
        'form': form,
        'titulo_pagina': f'Editar Usuário: {usuario_para_editar.get_full_name()}'
    }
    return render(request, 'gestao/usuario_form.html', context)

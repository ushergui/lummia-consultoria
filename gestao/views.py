# gestao/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_cliente_required, administrador_required
from accounts.models import CustomUser
from .models import Empresa
from .forms import (
    AdicionarUsuarioForm, EditarUsuarioForm, EmpresaForm, 
    AdminCriaUsuarioForm, AdminEditaUsuarioForm
)

# --- Views do Admin da Plataforma ---

@login_required
@administrador_required
def gerenciar_empresas_view(request):
    empresas = Empresa.objects.all()
    return render(request, 'gestao/gerenciar_empresas.html', {'empresas': empresas})

@login_required
@administrador_required
def criar_empresa_view(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'gestao/empresa_form.html', {'form': form, 'titulo_pagina': 'Adicionar Nova Empresa'})

@login_required
@administrador_required
def editar_empresa_view(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'gestao/empresa_form.html', {'form': form, 'titulo_pagina': f'Editar Empresa: {empresa.nome}'})

@login_required
@administrador_required
def gerenciar_todos_usuarios_view(request):
    usuarios = CustomUser.objects.all().order_by('empresa__nome', 'username')
    return render(request, 'gestao/gerenciar_todos_usuarios.html', {'usuarios': usuarios})

@login_required
@administrador_required
def criar_usuario_plataforma_view(request):
    if request.method == 'POST':
        form = AdminCriaUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_todos_usuarios')
    else:
        form = AdminCriaUsuarioForm()
    return render(request, 'gestao/usuario_plataforma_form.html', {'form': form, 'titulo_pagina': 'Adicionar Novo Usuário na Plataforma'})

@login_required
@administrador_required
def editar_usuario_plataforma_view(request, pk):
    usuario = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = AdminEditaUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_todos_usuarios')
    else:
        form = AdminEditaUsuarioForm(instance=usuario)
    return render(request, 'gestao/usuario_plataforma_form.html', {'form': form, 'titulo_pagina': f'Editar Usuário: {usuario.username}'})


# --- Views do Admin Cliente (já existentes) ---

@login_required
@admin_cliente_required
def gerenciar_usuarios_view(request):
    usuarios_da_empresa = CustomUser.objects.filter(empresa=request.user.empresa)
    context = {'usuarios': usuarios_da_empresa}
    return render(request, 'gestao/gerenciar_usuarios.html', context)

@login_required
@admin_cliente_required
def adicionar_usuario_view(request):
    if request.method == 'POST':
        form = AdicionarUsuarioForm(request.POST)
        if form.is_valid():
            novo_usuario = form.save(commit=False)
            novo_usuario.empresa = request.user.empresa
            novo_usuario.tipo_perfil = 'SERVIDOR_CLIENTE'
            novo_usuario.save()
            return redirect('gerenciar_usuarios')
    else:
        form = AdicionarUsuarioForm()
    context = {'form': form, 'titulo_pagina': 'Adicionar Novo Usuário à Equipe'}
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
    context = {'form': form, 'titulo_pagina': f'Editar Usuário: {usuario_para_editar.get_full_name()}'}
    return render(request, 'gestao/usuario_form.html', context)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Adiciona os seus campos customizados ao painel de administração
    # para que possam ser vistos e editados.
    
    # Campos que aparecem na lista de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_perfil', 'empresa')
    
    # Campos que aparecem no formulário de edição do usuário
    # Vamos adicionar os campos 'tipo_perfil' e 'empresa' ao fieldset 'Personal info'
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('tipo_perfil', 'empresa'),
        }),
    )
    
    # Adiciona os campos ao formulário de criação de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': ('tipo_perfil', 'empresa'),
        }),
    )

# Registra o seu modelo CustomUser com a configuração customizada
admin.site.register(CustomUser, CustomUserAdmin)
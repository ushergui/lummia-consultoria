# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from gestao.models import Empresa # Importe o modelo Empresa

class CustomUser(AbstractUser):
    class TipoPerfil(models.TextChoices):
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        ADMIN_CLIENTE = 'ADMIN_CLIENTE', 'Admin Cliente'
        SERVIDOR_CLIENTE = 'SERVIDOR_CLIENTE', 'Servidor Cliente'

    tipo_perfil = models.CharField(
        max_length=20,
        choices=TipoPerfil.choices,
        default=TipoPerfil.SERVIDOR_CLIENTE,
        verbose_name="Tipo de Perfil"
    )

    # Adicione este campo para associar o usuário a uma empresa
    # `null=True` e `blank=True` permitem que Administradores não pertençam a nenhuma empresa
    empresa = models.ForeignKey(
        Empresa, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='usuarios'
    )

    def __str__(self):
        return self.username

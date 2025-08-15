# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# O nome da classe deve ser exatamente 'CustomUser'
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

    def __str__(self):
        return self.username
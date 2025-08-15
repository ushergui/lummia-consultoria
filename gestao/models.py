# gestao/models.py
from django.db import models

class Empresa(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome da Empresa/Clínica")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome

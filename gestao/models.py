# gestao/models.py
from django.db import models

class Ferramenta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    # O 'slug' é um identificador para usar na URL (ex: 'dimensionamento-enfermagem')
    slug = models.SlugField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome

class Empresa(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome da Empresa/Clínica")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    data_criacao = models.DateTimeField(auto_now_add=True)
    # Adicione este campo para criar a relação Muitos-para-Muitos
    ferramentas_contratadas = models.ManyToManyField(
        Ferramenta, 
        blank=True,
        verbose_name="Ferramentas Contratadas"
    )

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome

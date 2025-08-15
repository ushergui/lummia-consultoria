# core/models.py
from django.db import models
from django.utils import timezone

class Noticia(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo")
    imagem = models.ImageField(upload_to='noticias/', verbose_name="Imagem de Capa")
    data_publicacao = models.DateTimeField(default=timezone.now, verbose_name="Data de Publicação")
    
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao'] # Ordena da mais nova para a mais antiga

    def __str__(self):
        return self.titulo

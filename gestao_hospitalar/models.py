from django.db import models
from gestao.models import Empresa
from django.utils import timezone
from django.conf import settings

# NOVO MODELO PARA O CID-10
class CID10(models.Model):
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código CID-10")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")

    class Meta:
        verbose_name = "Doença (CID-10)"
        verbose_name_plural = "Doenças (CID-10)"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class Ala(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da Ala")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="alas")

    class Meta:
        verbose_name = "Ala"
        verbose_name_plural = "Alas"
        unique_together = ('nome', 'empresa')

    def __str__(self):
        return self.nome

class Quarto(models.Model):
    numero = models.CharField(max_length=20, verbose_name="Número do Quarto")
    ala = models.ForeignKey(Ala, on_delete=models.CASCADE, related_name="quartos")

    class Meta:
        verbose_name = "Quarto"
        verbose_name_plural = "Quartos"
        unique_together = ('numero', 'ala')

    def __str__(self):
        return f"{self.numero} ({self.ala.nome})"

class Leito(models.Model):
    numero = models.CharField(max_length=20, verbose_name="Número do Leito")
    quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, related_name="leitos")

    class Meta:
        verbose_name = "Leito"
        verbose_name_plural = "Leitos"
        unique_together = ('numero', 'quarto')

    def __str__(self):
        return f"Leito {self.numero} - Quarto {self.quarto.numero}"

class Paciente(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome Completo do Paciente")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    
    # CAMPOS ATUALIZADOS PARA USAR O MODELO CID10
    hipotese_diagnostica_principal = models.ForeignKey(
        CID10, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="pacientes_com_diag_principal",
        verbose_name="Hipótese Diagnóstica (CID-10 Principal)"
    )
    diagnosticos_complementares = models.ManyToManyField(
        CID10, 
        blank=True,
        related_name="pacientes_com_diag_complementar",
        verbose_name="Diagnósticos Complementares (CID-10)"
    )
    
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="pacientes")
    leito = models.OneToOneField(Leito, on_delete=models.SET_NULL, null=True, blank=True, related_name="paciente_alocado")

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

    def __str__(self):
        return self.nome

class AvaliacaoFugulin(models.Model):
    # Relacionamentos
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='avaliacoes_fugulin')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    data_avaliacao = models.DateField(default=timezone.now)

    # 9 Áreas de Cuidado do Instrumento de Fugulin
    CHOICES_PONTUACAO = [(1, '1'), (2, '2'), (3, '3'), (4, '4')]
    
    estado_mental = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Estado Mental")
    oxigenacao = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Oxigenação")
    sinais_vitais = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Sinais Vitais")
    motilidade = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Motilidade")
    deambulacao = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Deambulação")
    alimentacao = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Alimentação")
    cuidado_corporal = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Cuidado Corporal")
    eliminacao = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Eliminação")
    terapeutica = models.IntegerField(choices=CHOICES_PONTUACAO, verbose_name="Terapêutica")
    
    # Campos calculados
    pontuacao_total = models.IntegerField(editable=False, null=True)
    categoria_cuidado = models.CharField(max_length=50, editable=False, null=True)

    class Meta:
        verbose_name = "Avaliação (Fugulin)"
        verbose_name_plural = "Avaliações (Fugulin)"
        unique_together = ('paciente', 'data_avaliacao') # Garante uma avaliação por dia por paciente
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f"Avaliação de {self.paciente.nome} em {self.data_avaliacao.strftime('%d/%m/%Y')}"

    def calcular_e_definir_categoria(self):
        """Calcula a pontuação total e define a categoria de cuidado."""
        indicadores = [
            self.estado_mental, self.oxigenacao, self.sinais_vitais,
            self.motilidade, self.deambulacao, self.alimentacao,
            self.cuidado_corporal, self.eliminacao, self.terapeutica
        ]
        self.pontuacao_total = sum(indicadores)

        # [cite_start]Pontuações baseadas no Artigo 01 [cite: 679, 680, 681]
        if self.pontuacao_total <= 14:
            self.categoria_cuidado = 'Cuidado Mínimo'
        elif self.pontuacao_total <= 20:
            self.categoria_cuidado = 'Cuidado Intermediário'
        elif self.pontuacao_total <= 26:
            self.categoria_cuidado = 'Cuidado de Alta Dependência'
        elif self.pontuacao_total <= 31:
            self.categoria_cuidado = 'Cuidado Semi-Intensivo'
        else:
            self.categoria_cuidado = 'Cuidado Intensivo'
    
    def save(self, *args, **kwargs):
        self.calcular_e_definir_categoria()
        super().save(*args, **kwargs)
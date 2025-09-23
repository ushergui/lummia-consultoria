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

class AreaCorporal(models.Model):
    """ Ex: Cabeça, Tórax, Abdômen """
    nome = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome

class AreaEspecifica(models.Model):
    """ Ex: Crânio, Couro Cabeludo (pertencem à Cabeça) """
    nome = models.CharField(max_length=100)
    area_corporal = models.ForeignKey(AreaCorporal, on_delete=models.CASCADE, related_name='areas_especificas')

    def __str__(self):
        return f"{self.area_corporal.nome} - {self.nome}"

class AchadoClinico(models.Model):
    """ Ex: Assimetria, Presença de lesões (pertencem ao Crânio) """
    descricao = models.CharField(max_length=255)
    area_especifica = models.ForeignKey(AreaEspecifica, on_delete=models.CASCADE, related_name='achados_clinicos')
    # O tipo de exame é um atributo do achado, pois um achado é resultado de um tipo de exame
    TIPO_EXAME_CHOICES = [('INSPECAO', 'Inspeção'), ('PALPACAO', 'Palpação'), ('AUSCULTA', 'Ausculta'), ('PERCUSSAO', 'Percussão')]
    tipo_exame = models.CharField(max_length=10, choices=TIPO_EXAME_CHOICES)

    def __str__(self):
        return self.descricao

# ====================================================================
# 2. MODELOS PARA AS TAXONOMIAS NANDA-I, NOC, NIC
# Baseado no livro "Ligações NANDA, NOC e NIC"
# ====================================================================

class DiagnosticoNANDA(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=255)
    definicao = models.TextField()
    # Mapeamento: Um achado clínico pode sugerir vários diagnósticos NANDA
    achados_relacionados = models.ManyToManyField(AchadoClinico, related_name='diagnosticos_sugeridos', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

class ResultadoNOC(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=255)
    definicao = models.TextField()
    # Ligação: Um diagnóstico NANDA pode ter vários resultados NOC esperados
    diagnosticos_nanda = models.ManyToManyField(DiagnosticoNANDA, related_name='resultados_noc', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

class IntervencaoNIC(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=255)
    definicao = models.TextField()
    # Ligação: Um resultado NOC é alcançado através de várias intervenções NIC
    resultados_noc = models.ManyToManyField(ResultadoNOC, related_name='intervencoes_nic', blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"

class AtividadeNIC(models.Model):
    descricao = models.TextField()
    intervencao = models.ForeignKey(IntervencaoNIC, on_delete=models.CASCADE, related_name='atividades')

    def __str__(self):
        # Retorna os primeiros 70 caracteres para não poluir o admin
        return self.descricao[:70] + '...' if len(self.descricao) > 70 else self.descricao

# ====================================================================
# 3. MODELOS PARA REGISTRAR A AVALIAÇÃO E O PLANO DE CUIDADOS DO PACIENTE
# Esta é a parte que será preenchida diariamente e persistida
# ====================================================================

class AvaliacaoSAE(models.Model):
    """ Registra uma avaliação completa de um paciente em um determinado dia. """
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='avaliacoes_sae')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    data_avaliacao = models.DateTimeField(default=timezone.now)
    
    # Etapa 3: Guarda os achados que o enfermeiro selecionou
    achados_selecionados = models.ManyToManyField(AchadoClinico, blank=True)
    
    # Etapa 5: Guarda o plano de cuidados definido
    diagnostico_nanda_selecionado = models.ForeignKey(DiagnosticoNANDA, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_finalizada = models.BooleanField(default=False)

    class Meta:
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f"SAE de {self.paciente.nome} em {self.data_avaliacao.strftime('%d/%m/%Y %H:%M')}"

class PlanoCuidado(models.Model):
    """ Armazena o progresso de uma intervenção (NIC) para uma avaliação específica. """
    avaliacao = models.ForeignKey(AvaliacaoSAE, on_delete=models.CASCADE, related_name='plano_de_cuidados')
    intervencao_nic = models.ForeignKey(IntervencaoNIC, on_delete=models.CASCADE)
    
    # JSONField é perfeito para guardar o estado das checkboxes (ID da atividade: True/False)
    progresso_atividades = models.JSONField(default=dict, blank=True)
    
    class Meta:
        unique_together = ('avaliacao', 'intervencao_nic')

    def __str__(self):
        return f"Plano para {self.intervencao_nic.titulo} na avaliação de {self.avaliacao.paciente.nome}"
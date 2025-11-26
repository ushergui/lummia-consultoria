from django.db import models

class Pergunta(models.Model):
    numero = models.IntegerField(unique=True, help_text="Número da pergunta (ex: 1, 2, 3)")
    texto = models.TextField()

    def __str__(self):
        return f"Pergunta {self.numero}"

class OpcaoResposta(models.Model):
    pergunta = models.ForeignKey(Pergunta, related_name='opcoes', on_delete=models.CASCADE)
    texto = models.CharField(max_length=10, help_text="Ex: 'SIM' ou 'NÃO'")
    risco_resultante = models.CharField(max_length=10, help_text="Ex: 'III', 'II', 'I', 'NA'")

    def __str__(self):
        return f"{self.pergunta.numero}: {self.texto} -> Risco {self.risco_resultante}"

class CNAE(models.Model):
    codigo = models.CharField(max_length=20, unique=True, primary_key=True)
    descricao = models.CharField(max_length=512)
    risco_base = models.CharField(max_length=10, help_text="I, II, III, NA, ou P")
    perguntas = models.ManyToManyField(Pergunta, blank=True, help_text="Perguntas associadas se o risco_base for 'P'")
    
    # NOVO CAMPO ADICIONADO AQUI
    dispensado_de_projeto = models.BooleanField(
        default=False, 
        help_text="Marca se uma atividade de Risco III é dispensada de aprovação de projeto arquitetônico (Anexo III)"
    )

    def __str__(self):
        return f"{self.codigo} - {self.risco_base}"
    
class ClassificacaoAmbiental(models.Model):
    """
    Tabela específica para o Decreto Municipal nº 6615 (Ambiental).
    Um único CNAE pode ter várias entradas aqui se tiver diferentes
    códigos DN COPAM ou especificidades.
    """
    cnae = models.ForeignKey(CNAE, on_delete=models.CASCADE, related_name='classificacoes_ambientais')
    
    # Coluna: NÍVEL AGREGAÇÃO CNAE (Atividade ou Subclasse)
    nivel_agregacao = models.CharField(max_length=50, blank=True, null=True)
    
    # Coluna: CÓDIGO DN COPAM (Ex: G-03-04-2, ou 'Não Listada')
    codigo_dn_copam = models.CharField(max_length=50, blank=True, null=True)
    
    # Coluna: DESCRIÇÃO DO CÓDIGO (Descrição específica da atividade ambiental)
    # Diferente da descrição padrão do IBGE que está no model CNAE
    descricao_atividade = models.TextField(verbose_name="Descrição da Atividade Ambiental")
    
    # Coluna: EXIGÊNCIA AMBIENTAL MUNICIPAL (Ex: Licença Ambiental, Dispensa, Não se aplica)
    exigencia_municipal = models.CharField(max_length=255, blank=True, null=True)
    
    # Coluna: NÍVEL DE RISCO (Ex: I, II, III)
    nivel_risco = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.cnae.codigo} - {self.codigo_dn_copam} ({self.nivel_risco})"
    

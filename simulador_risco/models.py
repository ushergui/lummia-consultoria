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
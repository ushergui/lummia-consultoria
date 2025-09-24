from django.core.management.base import BaseCommand
from django.db import transaction
from gestao_hospitalar.models import (
    # Modelos de Avaliação e Plano de Cuidados
    PlanoCuidado, AvaliacaoSAE,
    # Modelos de Taxonomia (serão recadastrados em produção)
    AtividadeNIC, IntervencaoNIC, ResultadoNOC, DiagnosticoNANDA,
    # Modelos do Exame Físico (serão recadastrados em produção)
    AchadoClinico, AreaEspecifica, TipoExame
    # Nota: Não apagaremos AreaCorporal, pois é um cadastro base e global.
)

class Command(BaseCommand):
    help = 'Limpa TODOS os dados de parametrização e avaliação da SAE. Use com cuidado em produção.'

    def add_arguments(self, parser):
        # Adiciona um argumento de confirmação para segurança
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirmação explícita para executar a limpeza de dados.',
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        if not kwargs['confirm']:
            self.stdout.write(self.style.ERROR(
                'Operação cancelada. Use a flag --confirm para executar a limpeza.'
            ))
            self.stdout.write(self.style.WARNING(
                'Exemplo de uso: python manage.py clean_sae_data --confirm'
            ))
            return

        self.stdout.write(self.style.WARNING('INICIANDO LIMPEZA DE DADOS DA SAE...'))

        # A ordem da exclusão é importante para respeitar as dependências (filhos primeiro)
        
        self.stdout.write('Limpando Planos de Cuidado e Avaliações SAE...')
        PlanoCuidado.objects.all().delete()
        AvaliacaoSAE.objects.all().delete()

        self.stdout.write('Limpando Taxonomias (NIC, NOC, NANDA)...')
        AtividadeNIC.objects.all().delete()
        IntervencaoNIC.objects.all().delete()
        ResultadoNOC.objects.all().delete()
        DiagnosticoNANDA.objects.all().delete()
        
        self.stdout.write('Limpando Estrutura do Exame Físico (Achados, Áreas, Tipos)...')
        AchadoClinico.objects.all().delete()
        AreaEspecifica.objects.all().delete()
        TipoExame.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            'Limpeza dos dados de parametrização e avaliação da SAE concluída com sucesso!'
        ))
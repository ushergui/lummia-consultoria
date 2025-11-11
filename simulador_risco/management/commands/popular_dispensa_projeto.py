# simulador_risco/management/commands/popular_dispensa_projeto.py

from django.core.management.base import BaseCommand
from simulador_risco.models import CNAE

class Command(BaseCommand):
    help = 'Atualiza os CNAEs de Risco III que são dispensados da aprovação de projeto arquitetônico, com base no Anexo III da Resolução.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando atualização de dispensa de projeto arquitetônico...'))

        # Lista de códigos CNAE (apenas números) do Anexo III da resolução
        cnaes_dispensados = [
            '3312103', '3600602', '4713002', '4713004', '4713005', '4722901',
            '4722902', '4729699', '4773300', '4789099', '4911600', '4930201',
            '4930202', '4930203', '5021101', '5021102', '5120000', '5211701',
            '5211799', '5212500', '5229099', '5240199', '5310501', '5310502',
            '6202300', '6203100', '7500100', '7729203', '7739002', '8621601',
            '8621602', '8690999', '8720499', '8730101', '8730199', '8800600',
            '9430800', '9602502'
        ]

        # Primeiro, garantimos que todos os CNAEs comecem com 'dispensado_de_projeto = False' para limpar dados antigos
        CNAE.objects.all().update(dispensado_de_projeto=False)
        self.stdout.write(self.style.NOTICE('Todos os CNAEs foram resetados para "não dispensado".'))

        # Agora, atualizamos apenas os CNAEs da lista
        cnaes_encontrados = CNAE.objects.filter(codigo__in=cnaes_dispensados)
        
        atualizados_count = cnaes_encontrados.update(dispensado_de_projeto=True)

        self.stdout.write(self.style.SUCCESS(f'{atualizados_count} CNAEs foram marcados como dispensados de projeto.'))

        # Verificação (Opcional, mas útil)
        codigos_encontrados = set(cnaes_encontrados.values_list('codigo', flat=True))
        codigos_nao_encontrados = set(cnaes_dispensados) - codigos_encontrados

        if codigos_nao_encontrados:
            self.stdout.write(self.style.WARNING('Os seguintes CNAEs da lista de dispensa não foram encontrados no banco de dados:'))
            for codigo in codigos_nao_encontrados:
                self.stdout.write(self.style.WARNING(f'- {codigo}'))
        else:
            self.stdout.write(self.style.SUCCESS('Todos os CNAEs da lista de dispensa foram encontrados e atualizados.'))

        self.stdout.write(self.style.SUCCESS('Atualização concluída!'))
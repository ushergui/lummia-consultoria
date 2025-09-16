import csv
from django.core.management.base import BaseCommand
from gestao_hospitalar.models import CID10

class Command(BaseCommand):
    help = 'Carrega a lista de doenças do CID-10 a partir de um arquivo CSV'

    def handle(self, *args, **kwargs):
        file_path = 'cid10.csv'
        self.stdout.write(self.style.SUCCESS(f'Iniciando o carregamento do arquivo {file_path}...'))

        try:
            with open(file_path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                cid10_objects = []
                for row in reader:
                    # Ignora códigos de categoria (ex: A00-A09) que não são diagnósticos finais
                    if '-' in row['codigo']:
                        continue
                    
                    cid10_objects.append(
                        CID10(
                            codigo=row['codigo'],
                            descricao=row['descricao']
                        )
                    )
                
                # Usa bulk_create para inserir todos de uma vez (muito mais rápido)
                CID10.objects.bulk_create(cid10_objects, ignore_conflicts=True)

            self.stdout.write(self.style.SUCCESS('Carregamento do CID-10 concluído com sucesso!'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo {file_path} não encontrado na raiz do projeto.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro: {e}'))
# Dentro de importar_dados_ses.py
import csv
from pathlib import Path
from django.core.management.base import BaseCommand
from simulador_risco.models import CNAE, Pergunta, OpcaoResposta

class Command(BaseCommand):
    help = 'Importa dados dos arquivos CSV da Resolução SES'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando importação...'))

        APP_DIR = Path(__file__).resolve().parent.parent.parent
        
        perguntas_csv = APP_DIR / 'dados' / 'perguntas.csv'
        opcoes_csv = APP_DIR / 'dados' / 'opcoes_resposta.csv'
        cnaes_csv = APP_DIR / 'dados' / 'cnaes.csv'
        cnae_perguntas_csv = APP_DIR / 'dados' / 'cnae_perguntas.csv'

        # Função auxiliar para limpar CNAEs
        def limpar_cnae(codigo_sujo):
            return ''.join(filter(str.isdigit, codigo_sujo))

        # 1. Importar Perguntas (sem alterações)
        with open(perguntas_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Pergunta.objects.get_or_create(
                    numero=row['numero'],
                    defaults={'texto': ' '.join(row['texto'].split())}
                )

        # 2. Importar Opções de Resposta (sem alterações)
        with open(opcoes_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pergunta = Pergunta.objects.get(numero=row['numero_pergunta'])
                OpcaoResposta.objects.get_or_create(
                    pergunta=pergunta,
                    texto=row['texto_resposta'],
                    defaults={'risco_resultante': row['risco_resultante']}
                )

        # 3. Importar CNAEs (COM CORREÇÃO)
        self.stdout.write("Importando CNAEs com códigos limpos...")
        with open(cnaes_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codigo_limpo = limpar_cnae(row['codigo'])
                if not codigo_limpo: # Pula linhas vazias se houver
                    continue
                
                CNAE.objects.get_or_create(
                    codigo=codigo_limpo, # SALVA O CÓDIGO SÓ COM NÚMEROS
                    defaults={
                        'descricao': row['descricao'],
                        'risco_base': row['risco_base']
                    }
                )

        # 4. Importar Relações M2M (COM CORREÇÃO)
        self.stdout.write("Importando relações com códigos limpos...")
        with open(cnae_perguntas_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    codigo_cnae_limpo = limpar_cnae(row['codigo_cnae'])
                    if not codigo_cnae_limpo:
                        continue

                    cnae = CNAE.objects.get(codigo=codigo_cnae_limpo) # BUSCA PELO CÓDIGO LIMPO
                    pergunta = Pergunta.objects.get(numero=row['numero_pergunta'])
                    cnae.perguntas.add(pergunta)
                except (CNAE.DoesNotExist, Pergunta.DoesNotExist) as e:
                    self.stdout.write(self.style.WARNING(f"Erro ao relacionar {row['codigo_cnae']} e {row['numero_pergunta']}: {e}"))

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
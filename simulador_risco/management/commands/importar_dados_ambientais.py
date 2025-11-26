import csv
import os
import re  # Importando regex para limpar o código
from django.core.management.base import BaseCommand
from django.conf import settings
from simulador_risco.models import CNAE, ClassificacaoAmbiental

class Command(BaseCommand):
    help = 'Importa os dados de Classificação Ambiental do Decreto 6.615 a partir de um CSV'

    def handle(self, *args, **kwargs):
        # Caminho do arquivo CSV
        file_path = os.path.join(settings.BASE_DIR, 'simulador_risco', 'dados', 'dados_ambientais.csv')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Arquivo não encontrado em: {file_path}'))
            return

        self.stdout.write(self.style.WARNING('Iniciando importação...'))

        # Limpa os dados antigos da tabela ambiental
        ClassificacaoAmbiental.objects.all().delete()
        self.stdout.write('Dados antigos apagados.')

        cont_sucesso = 0
        cont_erro = 0

        # Função auxiliar para deixar apenas números
        def limpar_cnae(valor):
            if not valor:
                return ""
            return re.sub(r'[^0-9]', '', str(valor))

        with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Normaliza os nomes das colunas do CSV (remove espaços e joga para maiúsculo)
            reader.fieldnames = [name.strip().upper() if name else '' for name in reader.fieldnames]

            for row in reader:
                # Pega o valor bruto do CSV
                codigo_cnae_bruto = row.get('CÓDIGO CNAE', '').strip()
                
                # LIMPEZA FUNDAMENTAL: Transforma "01.11-3/01" em "0111301"
                codigo_cnae_limpo = limpar_cnae(codigo_cnae_bruto)

                # Mapeamento das outras colunas
                nivel_agregacao = row.get('NÍVEL AGREGAÇÃO', row.get('NÍVEL AGREGAÇÃO CNAE', '')).strip()
                codigo_dn_copam = row.get('CÓDIGO DN COPAM', '').strip()
                
                # Tenta pegar a descrição (lida com possíveis variações no cabeçalho)
                descricao_atividade = row.get('DESCRIÇÃO DO CÓDIGO', '').strip()
                if not descricao_atividade:
                     for key in row.keys():
                         if key and 'DESCRIÇÃO' in key and 'CÓDIGO' in key:
                             descricao_atividade = row[key].strip()
                             break

                exigencia = row.get('EXIGÊNCIA AMBIENTAL', row.get('EXIGÊNCIA AMBIENTAL MUNICIPAL', '')).strip()
                
                risco = row.get('NÍVEL DE RISCO', '').strip()

                if codigo_cnae_limpo:
                    try:
                        # Agora busca pelo código limpo (igual ao banco)
                        cnae_obj = CNAE.objects.get(codigo=codigo_cnae_limpo)
                        
                        ClassificacaoAmbiental.objects.create(
                            cnae=cnae_obj,
                            nivel_agregacao=nivel_agregacao,
                            codigo_dn_copam=codigo_dn_copam,
                            descricao_atividade=descricao_atividade,
                            exigencia_municipal=exigencia,
                            nivel_risco=risco
                        )
                        cont_sucesso += 1

                    except CNAE.DoesNotExist:
                        # Mostra o código formatado no erro para facilitar sua leitura, mas avisa do limpo
                        # self.stdout.write(self.style.WARNING(f'CNAE não encontrado: {codigo_cnae_bruto} (Limpo: {codigo_cnae_limpo})'))
                        cont_erro += 1
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Erro linha {codigo_cnae_bruto}: {e}'))
                        cont_erro += 1

        self.stdout.write(self.style.SUCCESS(f'Concluído! Importados: {cont_sucesso}. Não encontrados/Erros: {cont_erro}'))
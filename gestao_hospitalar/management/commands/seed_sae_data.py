from django.core.management.base import BaseCommand
from django.db import transaction
from gestao_hospitalar.models import (
    AreaCorporal, AreaEspecifica, AchadoClinico,
    DiagnosticoNANDA, ResultadoNOC, IntervencaoNIC, AtividadeNIC
)

class Command(BaseCommand):
    help = 'Popula o banco de dados com uma base de dados expandida para o módulo SAE.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Limpando dados SAE existentes...'))
        # Limpa os dados para garantir um estado limpo a cada execução
        AtividadeNIC.objects.all().delete()
        IntervencaoNIC.objects.all().delete()
        ResultadoNOC.objects.all().delete()
        DiagnosticoNANDA.objects.all().delete()
        AchadoClinico.objects.all().delete()
        AreaEspecifica.objects.all().delete()
        AreaCorporal.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Limpeza concluída.'))

        self.stdout.write(self.style.SUCCESS('Criando nova base de dados de teste para SAE...'))

        # --- 1. Exame Físico ---
        # Áreas Corporais
        cabeça = AreaCorporal.objects.create(nome='Cabeça e Pescoço')
        torax = AreaCorporal.objects.create(nome='Tórax')
        abdome = AreaCorporal.objects.create(nome='Abdômen')
        membros_superiores = AreaCorporal.objects.create(nome='Membros Superiores')
        # --- NOVO ITEM ADICIONADO ---
        membros_inferiores = AreaCorporal.objects.create(nome='Membros Inferiores')

        # Áreas Específicas
        couro_cabeludo = AreaEspecifica.objects.create(nome='Couro Cabeludo', area_corporal=cabeça)
        pele_mmss = AreaEspecifica.objects.create(nome='Pele e Tegumento (MMSS)', area_corporal=membros_superiores)
        pulmoes = AreaEspecifica.objects.create(nome='Pulmões', area_corporal=torax)
        parede_abdominal = AreaEspecifica.objects.create(nome='Parede Abdominal', area_corporal=abdome)
        # --- NOVOS ITENS ADICIONADOS ---
        olhos = AreaEspecifica.objects.create(nome='Olhos', area_corporal=cabeça)
        boca_faringe = AreaEspecifica.objects.create(nome='Boca e Faringe', area_corporal=cabeça)
        coracao = AreaEspecifica.objects.create(nome='Coração', area_corporal=torax)
        pele_mmii = AreaEspecifica.objects.create(nome='Pele e Tegumento (MMII)', area_corporal=membros_inferiores)
        pulsos_perifericos = AreaEspecifica.objects.create(nome='Pulsos Periféricos (MMII)', area_corporal=membros_inferiores)
        
        # Achados Clínicos
        achado_lesao_cabeludo = AchadoClinico.objects.create(descricao='Presença de lesões ou descamação', area_especifica=couro_cabeludo, tipo_exame='INSPECAO')
        achado_pele_seca_mmss = AchadoClinico.objects.create(descricao='Pele seca e sem elasticidade', area_especifica=pele_mmss, tipo_exame='PALPACAO')
        achado_sibilos = AchadoClinico.objects.create(descricao='Presença de sibilos', area_especifica=pulmoes, tipo_exame='AUSCULTA')
        achado_ferida_cirurgica = AchadoClinico.objects.create(descricao='Ferida cirúrgica com sinais flogísticos', area_especifica=parede_abdominal, tipo_exame='INSPECAO')
        # --- NOVOS ITENS ADICIONADOS ---
        achado_mucosa_palida = AchadoClinico.objects.create(descricao='Mucosas oculares pálidas', area_especifica=olhos, tipo_exame='INSPECAO')
        achado_mucosa_oral_seca = AchadoClinico.objects.create(descricao='Mucosa oral ressecada', area_especifica=boca_faringe, tipo_exame='INSPECAO')
        achado_bulhas_arritmicas = AchadoClinico.objects.create(descricao='Bulhas cardíacas arrítmicas', area_especifica=coracao, tipo_exame='AUSCULTA')
        achado_edema_mmii = AchadoClinico.objects.create(descricao='Presença de edema (Cacifo positivo)', area_especifica=pele_mmii, tipo_exame='PALPACAO')
        achado_pulsos_diminuidos = AchadoClinico.objects.create(descricao='Pulsos pediosos diminuídos ou ausentes', area_especifica=pulsos_perifericos, tipo_exame='PALPACAO')

        # --- 2. Taxonomias (NANDA, NOC, NIC) ---
        
        # NANDA (Existentes + Novos)
        nanda_integridade_pele = DiagnosticoNANDA.objects.create(codigo='00046', titulo='Integridade da pele prejudicada', definicao='Epiderme e/ou derme alteradas.')
        nanda_risco_infeccao = DiagnosticoNANDA.objects.create(codigo='00004', titulo='Risco de infecção', definicao='Risco aumentado de ser invadido por organismos patogênicos.')
        nanda_padrao_respiratorio = DiagnosticoNANDA.objects.create(codigo='00032', titulo='Padrão respiratório ineficaz', definicao='Inspiração e/ou expiração que não proporciona ventilação adequada.')
        # --- NOVOS ITENS ADICIONADOS ---
        nanda_volume_liquidos = DiagnosticoNANDA.objects.create(codigo='00026', titulo='Volume de líquidos excessivo', definicao='Aumento da retenção de líquidos isotônicos.')
        nanda_perfusao_periferica = DiagnosticoNANDA.objects.create(codigo='00204', titulo='Perfusão tissular periférica ineficaz', definicao='Diminuição da circulação sanguínea para a periferia, que pode comprometer a saúde.')
        nanda_mucosa_oral = DiagnosticoNANDA.objects.create(codigo='00045', titulo='Mucosa oral prejudicada', definicao='Lesão nos lábios, tecidos moles, e/ou orofaringe.')

        # NOC (Existentes + Novos)
        noc_integridade_tissular = ResultadoNOC.objects.create(codigo='1101', titulo='Integridade tissular: pele e mucosas', definicao='Integridade estrutural e função fisiológica normal da pele e das membranas mucosas.')
        noc_cicatrizacao_ferida = ResultadoNOC.objects.create(codigo='1102', titulo='Cicatrização de feridas: primeira intenção', definicao='A magnitude da regeneração de células e tecidos.')
        noc_controle_risco = ResultadoNOC.objects.create(codigo='1902', titulo='Controle de risco', definicao='Ações para prevenir, eliminar ou reduzir ameaças à saúde.')
        noc_estado_respiratorio = ResultadoNOC.objects.create(codigo='0415', titulo='Estado respiratório', definicao='Movimento do ar para dentro e para fora dos pulmões.')
        # --- NOVOS ITENS ADICIONADOS ---
        noc_equilibrio_hidrico = ResultadoNOC.objects.create(codigo='0601', titulo='Equilíbrio hídrico', definicao='Equilíbrio de água nos compartimentos intracelular e extracelular do corpo.')
        noc_perfusao_tissular = ResultadoNOC.objects.create(codigo='0407', titulo='Perfusão tissular: periférica', definicao='Adequação do fluxo sanguíneo através dos pequenos vasos das extremidades para manter a função tecidual.')
        noc_saude_oral = ResultadoNOC.objects.create(codigo='1100', titulo='Saúde oral', definicao='Condição dos lábios, da boca, dos dentes, da gengiva e da língua.')

        # NIC (Existentes + Novos)
        nic_vigilancia_pele = IntervencaoNIC.objects.create(codigo='3590', titulo='Vigilância da pele', definicao='Coleta e análise de dados do paciente para manter a integridade da pele.')
        nic_cuidado_lesoes = IntervencaoNIC.objects.create(codigo='3660', titulo='Cuidado de lesões', definicao='Prevenção de complicações e promoção da cicatrização de feridas.')
        nic_controle_infeccao = IntervencaoNIC.objects.create(codigo='6540', titulo='Controle de infecções', definicao='Minimizar a aquisição e transmissão de agentes infecciosos.')
        nic_monitoracao_respiratoria = IntervencaoNIC.objects.create(codigo='3350', titulo='Monitoração respiratória', definicao='Coleta e análise de dados para garantir a permeabilidade das vias aéreas.')
        # --- NOVOS ITENS ADICIONADOS ---
        nic_controle_hidrico = IntervencaoNIC.objects.create(codigo='4120', titulo='Controle hídrico', definicao='Coleta e análise dos dados do paciente para regular o equilíbrio hídrico.')
        nic_cuidados_circulatorios = IntervencaoNIC.objects.create(codigo='4066', titulo='Cuidados circulatórios: insuficiência arterial', definicao='Promoção da circulação arterial.')
        nic_manutencao_saude_oral = IntervencaoNIC.objects.create(codigo='1710', titulo='Manutenção da saúde oral', definicao='Manutenção e promoção da higiene oral e da saúde dentária para o paciente.')
        
        # Atividades NIC
        AtividadeNIC.objects.create(descricao='Inspecionar a pele do paciente quanto à presença de rubor, calor ou drenagem.', intervencao=nic_vigilancia_pele)
        AtividadeNIC.objects.create(descricao='Monitorar a cor e a temperatura da pele.', intervencao=nic_vigilancia_pele)
        AtividadeNIC.objects.create(descricao='Limpar a ferida com solução apropriada.', intervencao=nic_cuidado_lesoes)
        AtividadeNIC.objects.create(descricao='Aplicar um curativo apropriado ao tipo de ferida.', intervencao=nic_cuidado_lesoes)
        AtividadeNIC.objects.create(descricao='Garantir a técnica de cuidado de feridas apropriada.', intervencao=nic_controle_infeccao)
        AtividadeNIC.objects.create(descricao='Auscultar os sons respiratórios, observando áreas de ventilação diminuída.', intervencao=nic_monitoracao_respiratoria)
        # --- NOVOS ITENS ADICIONADOS ---
        AtividadeNIC.objects.create(descricao='Pesar o paciente diariamente e monitorar tendências.', intervencao=nic_controle_hidrico)
        AtividadeNIC.objects.create(descricao='Monitorar ingesta e eliminações (balanço hídrico).', intervencao=nic_controle_hidrico)
        AtividadeNIC.objects.create(descricao='Realizar avaliação compreensiva da circulação periférica (pulsos, edema, enchimento capilar, cor, temperatura).', intervencao=nic_cuidados_circulatorios)
        AtividadeNIC.objects.create(descricao='Inspecionar a pele quanto à presença de úlceras arteriais ou lacerações teciduais.', intervencao=nic_cuidados_circulatorios)
        AtividadeNIC.objects.create(descricao='Monitorar lábios, língua e mucosas orais quanto à cor, umidade e integridade.', intervencao=nic_manutencao_saude_oral)
        AtividadeNIC.objects.create(descricao='Aplicar lubrificante nos lábios, conforme necessário.', intervencao=nic_manutencao_saude_oral)

        # --- 3. Mapeamentos e Ligações ---
        # Achados -> NANDA
        achado_lesao_cabeludo.diagnosticos_sugeridos.add(nanda_integridade_pele)
        achado_pele_seca_mmss.diagnosticos_sugeridos.add(nanda_integridade_pele)
        achado_ferida_cirurgica.diagnosticos_sugeridos.add(nanda_integridade_pele, nanda_risco_infeccao)
        achado_sibilos.diagnosticos_sugeridos.add(nanda_padrao_respiratorio)
        # --- NOVAS LIGAÇÕES ---
        achado_edema_mmii.diagnosticos_sugeridos.add(nanda_volume_liquidos)
        achado_pulsos_diminuidos.diagnosticos_sugeridos.add(nanda_perfusao_periferica)
        achado_mucosa_oral_seca.diagnosticos_sugeridos.add(nanda_mucosa_oral)
        
        # NANDA -> NOC
        nanda_integridade_pele.resultados_noc.add(noc_integridade_tissular, noc_cicatrizacao_ferida)
        nanda_risco_infeccao.resultados_noc.add(noc_controle_risco)
        nanda_padrao_respiratorio.resultados_noc.add(noc_estado_respiratorio)
        # --- NOVAS LIGAÇÕES ---
        nanda_volume_liquidos.resultados_noc.add(noc_equilibrio_hidrico)
        nanda_perfusao_periferica.resultados_noc.add(noc_perfusao_tissular)
        nanda_mucosa_oral.resultados_noc.add(noc_saude_oral, noc_integridade_tissular)

        # NOC -> NIC
        noc_integridade_tissular.intervencoes_nic.add(nic_vigilancia_pele)
        noc_cicatrizacao_ferida.intervencoes_nic.add(nic_cuidado_lesoes)
        noc_controle_risco.intervencoes_nic.add(nic_controle_infeccao)
        noc_estado_respiratorio.intervencoes_nic.add(nic_monitoracao_respiratoria)
        # --- NOVAS LIGAÇÕES ---
        noc_equilibrio_hidrico.intervencoes_nic.add(nic_controle_hidrico)
        noc_perfusao_tissular.intervencoes_nic.add(nic_cuidados_circulatorios)
        noc_saude_oral.intervencoes_nic.add(nic_manutencao_saude_oral)

        self.stdout.write(self.style.SUCCESS('Nova base de dados de teste da SAE foi criada com sucesso!'))
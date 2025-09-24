from django.urls import path
from . import views

app_name = 'gestao_hospitalar'

urlpatterns = [
    path('', views.HospitalDashboardView.as_view(), name='dashboard'),
    path('sae/parametrizacao/', views.SAEParametrizacaoView.as_view(), name='sae_parametrizacao'),

    # URLs para Ala
    path('alas/', views.AlaListView.as_view(), name='ala_list'),
    path('alas/nova/', views.AlaCreateView.as_view(), name='ala_create'),
    path('alas/<int:pk>/editar/', views.AlaUpdateView.as_view(), name='ala_update'),
    path('alas/<int:pk>/excluir/', views.AlaDeleteView.as_view(), name='ala_delete'),
    
    # URLs para Quarto
    path('quartos/', views.QuartoListView.as_view(), name='quarto_list'),
    path('quartos/novo/', views.QuartoCreateView.as_view(), name='quarto_create'),
    path('quartos/<int:pk>/editar/', views.QuartoUpdateView.as_view(), name='quarto_update'),
    path('quartos/<int:pk>/excluir/', views.QuartoDeleteView.as_view(), name='quarto_delete'),

    # URLs para Leito
    path('leitos/', views.LeitoListView.as_view(), name='leito_list'),
    path('leitos/novo/', views.LeitoCreateView.as_view(), name='leito_create'),
    path('leitos/<int:pk>/editar/', views.LeitoUpdateView.as_view(), name='leito_update'),
    path('leitos/<int:pk>/excluir/', views.LeitoDeleteView.as_view(), name='leito_delete'),

    # URLs para Paciente
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/novo/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('pacientes/<int:pk>/excluir/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    path('avaliacoes/', views.ListaPacientesParaAvaliacaoView.as_view(), name='paciente_avaliacao_list'),
    path('paciente/<int:pk>/avaliar/', views.AvaliarPacienteView.as_view(), name='paciente_avaliar'),
    path('paciente/<int:pk>/alta/', views.PacienteAltaView.as_view(), name='paciente_alta_confirm'),

    path('sae/', views.SAEDashboardView.as_view(), name='sae_dashboard'),
    path('paciente/<int:paciente_pk>/sae/avaliar/', views.SAEWizardView.as_view(), name='sae_wizard'),

# AreaCorporal
    path('areas-corporais/', views.AreaCorporalListView.as_view(), name='area_corporal_list'),
    path('areas-corporais/nova/', views.AreaCorporalCreateView.as_view(), name='area_corporal_create'),
    path('areas-corporais/<int:pk>/editar/', views.AreaCorporalUpdateView.as_view(), name='area_corporal_update'),
    path('areas-corporais/<int:pk>/excluir/', views.AreaCorporalDeleteView.as_view(), name='area_corporal_delete'),
    # TipoExame
    path('tipos-exame/', views.TipoExameListView.as_view(), name='tipo_exame_list'),
    path('tipos-exame/novo/', views.TipoExameCreateView.as_view(), name='tipo_exame_create'),
    path('tipos-exame/<int:pk>/editar/', views.TipoExameUpdateView.as_view(), name='tipo_exame_update'),
    path('tipos-exame/<int:pk>/excluir/', views.TipoExameDeleteView.as_view(), name='tipo_exame_delete'),
    # AreaEspecifica
    path('areas-especificas/', views.AreaEspecificaListView.as_view(), name='area_especifica_list'),
    path('areas-especificas/nova/', views.AreaEspecificaCreateView.as_view(), name='area_especifica_create'),
    path('areas-especificas/<int:pk>/editar/', views.AreaEspecificaUpdateView.as_view(), name='area_especifica_update'),
    path('areas-especificas/<int:pk>/excluir/', views.AreaEspecificaDeleteView.as_view(), name='area_especifica_delete'),
    # AchadoClinico
    path('achados-clinicos/', views.AchadoClinicoListView.as_view(), name='achado_clinico_list'),
    path('achados-clinicos/novo/', views.AchadoClinicoCreateView.as_view(), name='achado_clinico_create'),
    path('achados-clinicos/<int:pk>/editar/', views.AchadoClinicoUpdateView.as_view(), name='achado_clinico_update'),
    path('achados-clinicos/<int:pk>/excluir/', views.AchadoClinicoDeleteView.as_view(), name='achado_clinico_delete'),
    # NANDA
    path('nanda/', views.DiagnosticoNANDAListView.as_view(), name='nanda_list'),
    path('nanda/novo/', views.DiagnosticoNANDACreateView.as_view(), name='nanda_create'),
    path('nanda/<int:pk>/editar/', views.DiagnosticoNANDAUpdateView.as_view(), name='nanda_update'),
    path('nanda/<int:pk>/excluir/', views.DiagnosticoNANDADeleteView.as_view(), name='nanda_delete'),
    # NOC
    path('noc/', views.ResultadoNOCListView.as_view(), name='noc_list'),
    path('noc/novo/', views.ResultadoNOCCreateView.as_view(), name='noc_create'),
    path('noc/<int:pk>/editar/', views.ResultadoNOCUpdateView.as_view(), name='noc_update'),
    path('noc/<int:pk>/excluir/', views.ResultadoNOCDeleteView.as_view(), name='noc_delete'),
    # NIC
    path('nic/', views.IntervencaoNICListView.as_view(), name='nic_list'),
    path('nic/novo/', views.IntervencaoNICCreateView.as_view(), name='nic_create'),
    path('nic/<int:pk>/editar/', views.IntervencaoNICUpdateView.as_view(), name='nic_update'),
    path('nic/<int:pk>/excluir/', views.IntervencaoNICDeleteView.as_view(), name='nic_delete'),
    
    # ==========================================================
    # URLs para o Módulo SAE - Fluxo de Avaliação
    # ==========================================================
    path('sae/', views.SAEDashboardView.as_view(), name='sae_dashboard'),
    path('paciente/<int:paciente_pk>/sae/avaliar/', views.SAEWizardView.as_view(), name='sae_wizard'),
    path('sae/paciente/<int:paciente_pk>/historico/', views.SAEHistoricoView.as_view(), name='sae_historico_paciente'),
    path('sae/avaliacao/<int:pk>/', views.SAEAvaliacaoDetailView.as_view(), name='sae_avaliacao_detail'),
    


]
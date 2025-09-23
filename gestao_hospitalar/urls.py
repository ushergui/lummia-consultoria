from django.urls import path
from . import views

app_name = 'gestao_hospitalar'

urlpatterns = [
    path('', views.HospitalDashboardView.as_view(), name='dashboard'),
    
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

    # URLs para API interna (usadas pelo JavaScript para carregar dados dinamicamente)
    path('api/areas-especificas/<int:area_corporal_id>/', views.get_areas_especificas_json, name='api_get_areas_especificas'),
    path('api/achados-clinicos/<int:area_especifica_id>/<str:tipo_exame>/', views.get_achados_clinicos_json, name='api_get_achados_clinicos'),
    path('api/sugerir-nanda/', views.sugerir_nanda_json, name='api_sugerir_nanda'),
    path('api/plano-cuidados/<int:nanda_id>/', views.get_plano_cuidados_json, name='api_get_plano_cuidados'),
    path('sae/avaliacao/<int:pk>/', views.SAEAvaliacaoDetailView.as_view(), name='sae_avaliacao_detail'),
    path('sae/paciente/<int:paciente_pk>/historico/', views.SAEHistoricoView.as_view(), name='sae_historico_paciente'),
    path('sae/plano/<int:plano_id>/toggle/', views.toggle_plano_atividade, name='api_plano_toggle'),
]
from django.urls import path
from . import views

# Este arquivo conterá APENAS as rotas da nossa API interna
urlpatterns = [
    path('areas-especificas/<int:area_corporal_id>/', views.get_areas_especificas_json, name='api_get_areas_especificas'),
    path('achados-clinicos/<int:area_especifica_id>/<str:tipo_exame>/', views.get_achados_clinicos_json, name='api_get_achados_clinicos'),
    path('sugerir-nanda/', views.sugerir_nanda_json, name='api_sugerir_nanda'),
    path('plano-cuidados/<int:nanda_id>/', views.get_plano_cuidados_json, name='api_get_plano_cuidados'),
    path('plano/<int:plano_id>/toggle/', views.toggle_plano_atividade, name='api_plano_toggle'),
    
]
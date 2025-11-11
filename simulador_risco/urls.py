from django.urls import path
from . import views

app_name = 'simulador_risco'

urlpatterns = [
    path('', views.pagina_simulador, name='simulador'),
    path('api/consultar-cnaes/', views.api_consultar_cnaes, name='api_consultar_cnaes'),
    path('api/consultar-cnpj/<str:cnpj>/', views.api_consultar_cnpj, name='api_consultar_cnpj'),
    path('api/buscar-cnae/', views.api_buscar_cnae, name='api_buscar_cnae'),
]
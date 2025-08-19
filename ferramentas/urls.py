# ferramentas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # URL genérica que captura o slug da ferramenta e o envia para a view
    path('<slug:ferramenta_slug>/', views.ferramenta_view, name='acessar_ferramenta'),
]

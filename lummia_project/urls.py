# lummia_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('accounts.urls')),
    path('gestao/', include('gestao.urls')), 
    path('ferramentas/', include('ferramentas.urls')),
    path('', include('core.urls')),
    path('hospital/', include('gestao_hospitalar.urls')),
    path("select2/", include("django_select2.urls")),
    path('hospital/api/', include('gestao_hospitalar.api_urls')),
    path('simulador-risco-ses/', include('simulador_risco.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

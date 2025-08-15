# accounts/urls.py
from django.urls import path
from .views import CustomLoginView, register_view, CustomLogoutView, dashboard_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registrar/', register_view, name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

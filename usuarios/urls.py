from django.urls import path
from . import views

urlpatterns = [
    path('fluxo-negocio/', views.phase_permissions, name='phase_permissions'),
]

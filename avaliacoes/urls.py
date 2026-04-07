from django.urls import path
from . import views

urlpatterns = [
    path('', views.avaliacao_list, name='avaliacao_list'),
    path('<int:pk>/', views.avaliacao_detail, name='avaliacao_detail'),
    path('projeto/<int:projeto_id>/avaliar/', views.avaliacao_create, name='avaliacao_create'),
    path('projeto/<int:projeto_id>/viabilidade/', views.viabilidade_create, name='viabilidade_create'),
    path('projeto/<int:projeto_id>/priorizar/', views.priorizacao_create, name='priorizacao_create'),
]

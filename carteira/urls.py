from django.urls import path
from . import views

urlpatterns = [
    path('', views.carteira_list, name='carteira_list'),
    path('<int:pk>/', views.carteira_detail, name='carteira_detail'),
    path('nova/', views.carteira_create, name='carteira_create'),
    path('<int:pk>/adicionar-projeto/', views.carteira_adicionar_projeto, name='carteira_adicionar_projeto'),
    path('<int:pk>/remover-projeto/<int:projeto_id>/', views.carteira_remover_projeto, name='carteira_remover_projeto'),
    path('<int:pk>/validar/', views.carteira_validar, name='carteira_validar'),
    path('<int:pk>/deliberar/', views.carteira_deliberar, name='carteira_deliberar'),
]

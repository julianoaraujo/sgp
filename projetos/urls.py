from django.urls import path
from . import views

urlpatterns = [
    path('projetos/', views.projeto_list, name='projeto_list'),
    path('projetos/<int:pk>/', views.projeto_detail, name='projeto_detail'),
    path('projetos/novo/', views.projeto_create, name='projeto_create'),
    path('projetos/<int:pk>/editar/', views.projeto_edit, name='projeto_edit'),
    path('projetos/<int:pk>/submeter/', views.projeto_submeter, name='projeto_submeter'),
]

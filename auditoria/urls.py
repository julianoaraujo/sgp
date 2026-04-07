from django.urls import path
from . import views

urlpatterns = [
    path('notificacoes/', views.notificacao_list, name='notificacao_list'),
    path('notificacoes/<int:pk>/lida/', views.notificacao_marcar_lida, name='notificacao_marcar_lida'),
    path('notificacoes/marcar-todas-lidas/', views.notificacao_marcar_todas_lidas, name='notificacao_marcar_todas_lidas'),
    path('notificacoes/<int:pk>/arquivar/', views.notificacao_arquivar, name='notificacao_arquivar'),
    path('notificacoes/<int:pk>/deletar/', views.notificacao_deletar, name='notificacao_deletar'),
]

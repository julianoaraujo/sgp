from django.contrib import admin
from .models import Avaliacao, CriterioAvaliacaoA, CriterioAvaliacaoB, Viabilidade, Priorizacao, CriterioPriorizacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'avaliador', 'status', 'pontuacao_etapa_a', 'pontuacao_etapa_b', 'pontuacao_parcial']
    list_filter = ['status', 'data_inicio']
    search_fields = ['projeto__titulo', 'avaliador__username']
    readonly_fields = ['data_inicio', 'pontuacao_parcial']


@admin.register(Viabilidade)
class ViabilidadeAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'analista', 'status', 'resultado', 'data_inicio']
    list_filter = ['status', 'resultado']
    search_fields = ['projeto__titulo', 'analista__username']
    readonly_fields = ['data_inicio']


@admin.register(Priorizacao)
class PriorizacaoAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'responsavel', 'pontuacao_etapa_c', 'complexidade', 'urgencia', 'impacto_estrategico']
    list_filter = ['complexidade', 'urgencia', 'impacto_estrategico']
    search_fields = ['projeto__titulo', 'responsavel__username']
    readonly_fields = ['data_priorizacao', 'pontuacao_total_projeto']

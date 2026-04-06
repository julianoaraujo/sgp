from django.contrib import admin
from .models import Projeto, Recurso, Indicador, Documento


class RecursoInline(admin.TabularInline):
    model = Recurso
    extra = 1


class IndicadorInline(admin.TabularInline):
    model = Indicador
    extra = 1


class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 0


@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'demandante', 'status', 'prioridade', 'pontuacao_total', 'data_submissao']
    list_filter = ['status', 'prioridade', 'ativo']
    search_fields = ['titulo', 'descricao', 'demandante__username']
    readonly_fields = ['data_criacao', 'data_atualizacao', 'data_submissao']
    date_hierarchy = 'data_criacao'
    inlines = [RecursoInline, IndicadorInline, DocumentoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'justificativa', 'objetivos', 'resultados_esperados')
        }),
        ('Responsáveis', {
            'fields': ('demandante', 'gerente_projeto')
        }),
        ('Status e Prioridade', {
            'fields': ('status', 'prioridade', 'pontuacao_total')
        }),
        ('Datas', {
            'fields': ('data_inicio_prevista', 'data_fim_prevista', 'data_inicio_real', 'data_fim_real', 'data_submissao', 'data_aceite')
        }),
        ('Orçamento', {
            'fields': ('orcamento_previsto', 'orcamento_realizado')
        }),
        ('Outras Informações', {
            'fields': ('observacoes', 'ativo', 'data_criacao', 'data_atualizacao')
        }),
    )

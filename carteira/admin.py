from django.contrib import admin
from .models import Carteira, ProjetoCarteira, Validacao, Deliberacao, Comunicacao, Aceite


class ProjetoCarteiraInline(admin.TabularInline):
    model = ProjetoCarteira
    extra = 0


@admin.register(Carteira)
class CarteiraAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'ano', 'periodo', 'status', 'gerente_portfolio', 'orcamento_total']
    list_filter = ['status', 'ano']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['data_criacao', 'data_atualizacao']
    inlines = [ProjetoCarteiraInline]


@admin.register(Validacao)
class ValidacaoAdmin(admin.ModelAdmin):
    list_display = ['carteira', 'validador', 'status', 'data_inicio']
    list_filter = ['status']
    search_fields = ['carteira__titulo', 'validador__username']


@admin.register(Deliberacao)
class DeliberacaoAdmin(admin.ModelAdmin):
    list_display = ['carteira', 'deliberador', 'status', 'data_deliberacao']
    list_filter = ['status']
    search_fields = ['carteira__titulo', 'deliberador__username']


@admin.register(Comunicacao)
class ComunicacaoAdmin(admin.ModelAdmin):
    list_display = ['assunto', 'tipo', 'status', 'remetente', 'destinatario', 'data_criacao']
    list_filter = ['tipo', 'status']
    search_fields = ['assunto', 'mensagem']


@admin.register(Aceite)
class AceiteAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'aceito_por', 'data_aceite']
    search_fields = ['projeto__titulo', 'aceito_por__username']

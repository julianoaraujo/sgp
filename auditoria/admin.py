from django.contrib import admin
from .models import AuditLog, HistoricoStatus, Notificacao, Anexo


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'acao', 'modelo', 'objeto_repr', 'timestamp']
    list_filter = ['acao', 'modelo', 'timestamp']
    search_fields = ['usuario__username', 'modelo', 'objeto_repr', 'mensagem']
    readonly_fields = ['usuario', 'acao', 'modelo', 'objeto_id', 'objeto_repr', 
                       'dados_anteriores', 'dados_novos', 'ip_address', 'user_agent', 
                       'mensagem', 'timestamp']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HistoricoStatus)
class HistoricoStatusAdmin(admin.ModelAdmin):
    list_display = ['projeto', 'status_anterior', 'status_novo', 'usuario', 'data_transicao']
    list_filter = ['status_anterior', 'status_novo', 'data_transicao']
    search_fields = ['projeto__titulo', 'usuario__username']
    readonly_fields = ['data_transicao']


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'status', 'destinatario', 'data_criacao']
    list_filter = ['tipo', 'status', 'data_criacao']
    search_fields = ['titulo', 'mensagem', 'destinatario__username']


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ['nome_original', 'tipo_mime', 'tamanho', 'usuario_upload', 'data_upload']
    list_filter = ['tipo_mime', 'data_upload']
    search_fields = ['nome_original', 'usuario_upload__username']

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
import json


class AuditLog(models.Model):
    ACAO_CHOICES = [
        ('CREATE', 'Criação'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('SUBMIT', 'Submissão'),
        ('APPROVE', 'Aprovação'),
        ('REJECT', 'Rejeição'),
        ('TRANSITION', 'Transição de Status'),
        ('VIEW', 'Visualização'),
        ('EXPORT', 'Exportação'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='logs_auditoria'
    )
    
    acao = models.CharField(max_length=15, choices=ACAO_CHOICES, db_index=True)
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    modelo = models.CharField(max_length=100, db_index=True)
    objeto_id = models.CharField(max_length=100)
    objeto_repr = models.CharField(max_length=200)
    
    dados_anteriores = models.JSONField(null=True, blank=True)
    dados_novos = models.JSONField(null=True, blank=True)
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    mensagem = models.TextField(blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['usuario', '-timestamp']),
            models.Index(fields=['modelo', 'objeto_id']),
            models.Index(fields=['acao', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
        permissions = [
            ('view_all_logs', 'Pode visualizar todos os logs'),
            ('export_logs', 'Pode exportar logs'),
        ]
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_acao_display()} - {self.modelo} - {self.timestamp}"
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise Exception("Logs de auditoria são imutáveis e não podem ser alterados")
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        raise Exception("Logs de auditoria são imutáveis e não podem ser excluídos")
    
    @classmethod
    def registrar(cls, usuario, acao, modelo, objeto_id, objeto_repr, 
                  dados_anteriores=None, dados_novos=None, 
                  ip_address=None, user_agent=None, mensagem=''):
        return cls.objects.create(
            usuario=usuario,
            acao=acao,
            modelo=modelo,
            objeto_id=str(objeto_id),
            objeto_repr=objeto_repr,
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos,
            ip_address=ip_address,
            user_agent=user_agent,
            mensagem=mensagem
        )


class HistoricoStatus(models.Model):
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='historico_status'
    )
    
    status_anterior = models.CharField(max_length=25)
    status_novo = models.CharField(max_length=25)
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    
    justificativa = models.TextField(blank=True)
    
    data_transicao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'historico_status'
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        ordering = ['-data_transicao']
        indexes = [
            models.Index(fields=['projeto', '-data_transicao']),
        ]
    
    def __str__(self):
        return f"{self.projeto.titulo}: {self.status_anterior} → {self.status_novo}"


class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('INFO', 'Informação'),
        ('ALERTA', 'Alerta'),
        ('URGENTE', 'Urgente'),
        ('SUCESSO', 'Sucesso'),
        ('ERRO', 'Erro'),
    ]
    
    STATUS_CHOICES = [
        ('NAO_LIDA', 'Não Lida'),
        ('LIDA', 'Lida'),
        ('ARQUIVADA', 'Arquivada'),
    ]
    
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='INFO')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='NAO_LIDA')
    
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    
    link = models.CharField(max_length=500, blank=True)
    
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'notificacoes'
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['destinatario', 'status', '-data_criacao']),
            models.Index(fields=['destinatario', '-data_criacao']),
        ]
    
    def __str__(self):
        return f"{self.titulo} para {self.destinatario.username}"
    
    def marcar_como_lida(self):
        from django.utils import timezone
        if self.status == 'NAO_LIDA':
            self.status = 'LIDA'
            self.data_leitura = timezone.now()
            self.save()


class Anexo(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    arquivo = models.FileField(upload_to='anexos/%Y/%m/')
    nome_original = models.CharField(max_length=255)
    tamanho = models.BigIntegerField()
    tipo_mime = models.CharField(max_length=100)
    
    usuario_upload = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'anexos'
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['-data_upload']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return self.nome_original

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Carteira(models.Model):
    STATUS_CHOICES = [
        ('EM_CONSOLIDACAO', 'Em Consolidação'),
        ('EM_VALIDACAO', 'Em Validação'),
        ('EM_DELIBERACAO', 'Em Deliberação'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]
    
    ano = models.IntegerField(db_index=True)
    periodo = models.CharField(max_length=50)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='EM_CONSOLIDACAO'
    )
    
    gerente_portfolio = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='carteiras_gerenciadas'
    )
    
    orcamento_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True
    )
    
    data_consolidacao = models.DateTimeField(null=True, blank=True)
    data_validacao = models.DateTimeField(null=True, blank=True)
    data_deliberacao = models.DateTimeField(null=True, blank=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)
    
    observacoes = models.TextField(blank=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'carteiras'
        verbose_name = 'Carteira de Projetos'
        verbose_name_plural = 'Carteiras de Projetos'
        ordering = ['-ano', '-data_criacao']
        unique_together = [['ano', 'periodo']]
        indexes = [
            models.Index(fields=['ano', 'periodo']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"Carteira {self.ano} - {self.periodo}"


class ProjetoCarteira(models.Model):
    carteira = models.ForeignKey(
        Carteira,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='carteiras'
    )
    
    posicao_ranking = models.IntegerField(null=True, blank=True)
    incluido_carteira = models.BooleanField(default=True)
    justificativa_inclusao = models.TextField(blank=True)
    
    data_inclusao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'projetos_carteira'
        verbose_name = 'Projeto na Carteira'
        verbose_name_plural = 'Projetos na Carteira'
        unique_together = [['carteira', 'projeto']]
        ordering = ['posicao_ranking', '-projeto__pontuacao_total']
        indexes = [
            models.Index(fields=['carteira', 'incluido_carteira']),
            models.Index(fields=['posicao_ranking']),
        ]
    
    def __str__(self):
        return f"{self.projeto.titulo} na {self.carteira}"


class Validacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]
    
    carteira = models.ForeignKey(
        Carteira,
        on_delete=models.CASCADE,
        related_name='validacoes'
    )
    validador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='validacoes_realizadas'
    )
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    parecer = models.TextField()
    recomendacoes = models.TextField(blank=True)
    ajustes_solicitados = models.TextField(blank=True)
    
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'validacoes'
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['carteira', 'status']),
        ]
    
    def __str__(self):
        return f"Validação da {self.carteira} por {self.validador.get_full_name()}"


class Deliberacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]
    
    carteira = models.ForeignKey(
        Carteira,
        on_delete=models.CASCADE,
        related_name='deliberacoes'
    )
    deliberador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='deliberacoes_realizadas'
    )
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    decisao = models.TextField()
    justificativa = models.TextField()
    observacoes = models.TextField(blank=True)
    
    data_deliberacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'deliberacoes'
        verbose_name = 'Deliberação'
        verbose_name_plural = 'Deliberações'
        ordering = ['-data_deliberacao']
        indexes = [
            models.Index(fields=['carteira', 'status']),
        ]
    
    def __str__(self):
        return f"Deliberação da {self.carteira} por {self.deliberador.get_full_name()}"


class Comunicacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ENVIADA', 'Enviada'),
        ('RECEBIDA', 'Recebida'),
    ]
    
    TIPO_CHOICES = [
        ('APROVACAO', 'Aprovação de Projeto'),
        ('REJEICAO', 'Rejeição de Projeto'),
        ('SOLICITACAO_INFO', 'Solicitação de Informações'),
        ('NOTIFICACAO', 'Notificação Geral'),
    ]
    
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='comunicacoes',
        null=True,
        blank=True
    )
    carteira = models.ForeignKey(
        Carteira,
        on_delete=models.CASCADE,
        related_name='comunicacoes',
        null=True,
        blank=True
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    remetente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='comunicacoes_enviadas'
    )
    destinatario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='comunicacoes_recebidas'
    )
    
    assunto = models.CharField(max_length=200)
    mensagem = models.TextField()
    
    data_envio = models.DateTimeField(null=True, blank=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'comunicacoes'
        verbose_name = 'Comunicação'
        verbose_name_plural = 'Comunicações'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['destinatario', 'status']),
            models.Index(fields=['projeto', 'tipo']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.assunto}"


class Aceite(models.Model):
    projeto = models.OneToOneField(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='aceite'
    )
    
    aceito_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='aceites_realizados'
    )
    
    termo_aceite = models.TextField()
    observacoes = models.TextField(blank=True)
    
    data_aceite = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'aceites'
        verbose_name = 'Aceite'
        verbose_name_plural = 'Aceites'
        ordering = ['-data_aceite']
    
    def __str__(self):
        return f"Aceite do projeto {self.projeto.titulo}"

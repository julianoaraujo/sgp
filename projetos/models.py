from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from decimal import Decimal


class Projeto(models.Model):
    STATUS_CHOICES = [
        ('RASCUNHO', 'Rascunho'),
        ('SUBMETIDO', 'Submetido'),
        ('EM_AVALIACAO', 'Em Avaliação'),
        ('EM_VIABILIDADE', 'Em Análise de Viabilidade'),
        ('EM_PRIORIZACAO', 'Em Priorização'),
        ('EM_CONSOLIDACAO', 'Em Consolidação'),
        ('EM_VALIDACAO', 'Em Validação'),
        ('EM_DELIBERACAO', 'Em Deliberação'),
        ('AGUARDANDO_COMUNICACAO', 'Aguardando Comunicação'),
        ('COMUNICADO', 'Comunicado'),
        ('ACEITO', 'Aceito'),
        ('REJEITADO', 'Rejeitado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    
    titulo = models.CharField(max_length=200, db_index=True)
    descricao = models.TextField()
    justificativa = models.TextField()
    objetivos = models.TextField()
    resultados_esperados = models.TextField()
    
    demandante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='projetos_demandados'
    )
    gerente_projeto = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projetos_gerenciados'
    )
    
    status = models.CharField(
        max_length=25,
        choices=STATUS_CHOICES,
        default='RASCUNHO',
        db_index=True
    )
    prioridade = models.CharField(
        max_length=10,
        choices=PRIORIDADE_CHOICES,
        null=True,
        blank=True
    )
    
    data_inicio_prevista = models.DateField(null=True, blank=True)
    data_fim_prevista = models.DateField(null=True, blank=True)
    data_inicio_real = models.DateField(null=True, blank=True)
    data_fim_real = models.DateField(null=True, blank=True)
    
    orcamento_previsto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True
    )
    orcamento_realizado = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        null=True,
        blank=True
    )
    
    pontuacao_total = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(110)]
    )
    
    data_submissao = models.DateTimeField(null=True, blank=True)
    data_aceite = models.DateTimeField(null=True, blank=True)
    
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'projetos'
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['status', 'ativo']),
            models.Index(fields=['demandante', 'status']),
            models.Index(fields=['data_submissao']),
            models.Index(fields=['-pontuacao_total']),
        ]
    
    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"
    
    def pode_transicionar_para(self, novo_status):
        transicoes_validas = {
            'RASCUNHO': ['SUBMETIDO'],
            'SUBMETIDO': ['EM_AVALIACAO', 'CANCELADO'],
            'EM_AVALIACAO': ['EM_VIABILIDADE', 'REJEITADO'],
            'EM_VIABILIDADE': ['EM_PRIORIZACAO', 'REJEITADO'],
            'EM_PRIORIZACAO': ['EM_CONSOLIDACAO', 'REJEITADO'],
            'EM_CONSOLIDACAO': ['EM_VALIDACAO'],
            'EM_VALIDACAO': ['EM_DELIBERACAO', 'EM_CONSOLIDACAO'],
            'EM_DELIBERACAO': ['AGUARDANDO_COMUNICACAO', 'REJEITADO'],
            'AGUARDANDO_COMUNICACAO': ['COMUNICADO'],
            'COMUNICADO': ['ACEITO'],
        }
        return novo_status in transicoes_validas.get(self.status, [])
    
    def submeter(self):
        if self.status == 'RASCUNHO':
            self.status = 'SUBMETIDO'
            self.data_submissao = timezone.now()
            self.save()
            return True
        return False


class Recurso(models.Model):
    TIPO_CHOICES = [
        ('HUMANO', 'Recurso Humano'),
        ('MATERIAL', 'Material'),
        ('FINANCEIRO', 'Financeiro'),
        ('TECNOLOGICO', 'Tecnológico'),
    ]
    
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='recursos'
    )
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    descricao = models.CharField(max_length=200)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    unidade = models.CharField(max_length=50)
    custo_unitario = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'recursos'
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['tipo', 'descricao']
    
    def __str__(self):
        return f"{self.descricao} - {self.projeto.titulo}"
    
    @property
    def custo_total(self):
        return self.quantidade * self.custo_unitario


class Indicador(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='indicadores'
    )
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    meta = models.CharField(max_length=100)
    valor_atual = models.CharField(max_length=100, blank=True)
    unidade_medida = models.CharField(max_length=50)
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'indicadores'
        verbose_name = 'Indicador'
        verbose_name_plural = 'Indicadores'
        ordering = ['nome']
    
    def __str__(self):
        return f"{self.nome} - {self.projeto.titulo}"


class Documento(models.Model):
    TIPO_CHOICES = [
        ('TERMO_ABERTURA', 'Termo de Abertura'),
        ('PLANO_PROJETO', 'Plano de Projeto'),
        ('CRONOGRAMA', 'Cronograma'),
        ('ORCAMENTO', 'Orçamento'),
        ('RELATORIO', 'Relatório'),
        ('ATA', 'Ata de Reunião'),
        ('OUTRO', 'Outro'),
    ]
    
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='documentos'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(
        upload_to='projetos/documentos/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx']
            )
        ]
    )
    
    usuario_upload = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'documentos'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-data_upload']
    
    def __str__(self):
        return f"{self.titulo} - {self.projeto.titulo}"

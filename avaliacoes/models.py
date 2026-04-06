from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Avaliacao(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('CONCLUIDA', 'Concluída'),
    ]
    
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='avaliacoes'
    )
    avaliador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='avaliacoes_realizadas'
    )
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    
    pontuacao_etapa_a = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        null=True,
        blank=True,
        help_text='Alinhamento Estratégico (0-25 pontos)'
    )
    
    pontuacao_etapa_b = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)],
        null=True,
        blank=True,
        help_text='Impacto e Benefícios (0-25 pontos)'
    )
    
    parecer_tecnico = models.TextField(blank=True)
    recomendacoes = models.TextField(blank=True)
    
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'avaliacoes'
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['projeto', 'status']),
            models.Index(fields=['avaliador', 'status']),
        ]
    
    def __str__(self):
        return f"Avaliação de {self.projeto.titulo} por {self.avaliador.get_full_name()}"
    
    @property
    def pontuacao_parcial(self):
        total = Decimal('0.00')
        if self.pontuacao_etapa_a:
            total += self.pontuacao_etapa_a
        if self.pontuacao_etapa_b:
            total += self.pontuacao_etapa_b
        return total


class CriterioAvaliacaoA(models.Model):
    avaliacao = models.ForeignKey(
        Avaliacao,
        on_delete=models.CASCADE,
        related_name='criterios_etapa_a'
    )
    criterio = models.CharField(max_length=200)
    pontuacao = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)]
    )
    justificativa = models.TextField()
    
    class Meta:
        db_table = 'criterios_avaliacao_a'
        verbose_name = 'Critério Etapa A'
        verbose_name_plural = 'Critérios Etapa A'
    
    def __str__(self):
        return f"{self.criterio} - {self.pontuacao}"


class CriterioAvaliacaoB(models.Model):
    avaliacao = models.ForeignKey(
        Avaliacao,
        on_delete=models.CASCADE,
        related_name='criterios_etapa_b'
    )
    criterio = models.CharField(max_length=200)
    pontuacao = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(25)]
    )
    justificativa = models.TextField()
    
    class Meta:
        db_table = 'criterios_avaliacao_b'
        verbose_name = 'Critério Etapa B'
        verbose_name_plural = 'Critérios Etapa B'
    
    def __str__(self):
        return f"{self.criterio} - {self.pontuacao}"


class Viabilidade(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANALISE', 'Em Análise'),
        ('CONCLUIDA', 'Concluída'),
    ]
    
    RESULTADO_CHOICES = [
        ('VIAVEL', 'Viável'),
        ('VIAVEL_COM_RESTRICOES', 'Viável com Restrições'),
        ('INVIAVEL', 'Inviável'),
    ]
    
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='analises_viabilidade'
    )
    analista = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='viabilidades_analisadas'
    )
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDENTE'
    )
    resultado = models.CharField(
        max_length=25,
        choices=RESULTADO_CHOICES,
        null=True,
        blank=True
    )
    
    viabilidade_tecnica = models.BooleanField(null=True)
    viabilidade_financeira = models.BooleanField(null=True)
    viabilidade_operacional = models.BooleanField(null=True)
    viabilidade_juridica = models.BooleanField(null=True)
    
    analise_tecnica = models.TextField(blank=True)
    analise_financeira = models.TextField(blank=True)
    analise_operacional = models.TextField(blank=True)
    analise_juridica = models.TextField(blank=True)
    
    riscos_identificados = models.TextField(blank=True)
    restricoes = models.TextField(blank=True)
    
    data_inicio = models.DateTimeField(auto_now_add=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'viabilidades'
        verbose_name = 'Análise de Viabilidade'
        verbose_name_plural = 'Análises de Viabilidade'
        ordering = ['-data_inicio']
        indexes = [
            models.Index(fields=['projeto', 'status']),
            models.Index(fields=['resultado']),
        ]
    
    def __str__(self):
        return f"Viabilidade de {self.projeto.titulo}"


class Priorizacao(models.Model):
    projeto = models.ForeignKey(
        'projetos.Projeto',
        on_delete=models.CASCADE,
        related_name='priorizacoes'
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='priorizacoes_realizadas'
    )
    
    pontuacao_etapa_c = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
        help_text='Critérios Ponderados (0-60 pontos)'
    )
    
    complexidade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1=Muito Baixa, 5=Muito Alta'
    )
    urgencia = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1=Muito Baixa, 5=Muito Alta'
    )
    impacto_estrategico = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='1=Muito Baixo, 5=Muito Alto'
    )
    
    recursos_disponiveis = models.BooleanField(default=False)
    dependencias_externas = models.BooleanField(default=False)
    
    justificativa = models.TextField()
    observacoes = models.TextField(blank=True)
    
    data_priorizacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'priorizacoes'
        verbose_name = 'Priorização'
        verbose_name_plural = 'Priorizações'
        ordering = ['-pontuacao_etapa_c', '-data_priorizacao']
        indexes = [
            models.Index(fields=['projeto']),
            models.Index(fields=['-pontuacao_etapa_c']),
        ]
    
    def __str__(self):
        return f"Priorização de {self.projeto.titulo} - {self.pontuacao_etapa_c} pontos"
    
    @property
    def pontuacao_total_projeto(self):
        avaliacao = self.projeto.avaliacoes.filter(status='CONCLUIDA').first()
        if avaliacao:
            return avaliacao.pontuacao_parcial + self.pontuacao_etapa_c
        return self.pontuacao_etapa_c


class CriterioPriorizacao(models.Model):
    priorizacao = models.ForeignKey(
        Priorizacao,
        on_delete=models.CASCADE,
        related_name='criterios'
    )
    criterio = models.CharField(max_length=200)
    peso = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    pontuacao = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    
    class Meta:
        db_table = 'criterios_priorizacao'
        verbose_name = 'Critério de Priorização'
        verbose_name_plural = 'Critérios de Priorização'
    
    def __str__(self):
        return f"{self.criterio} - Peso: {self.peso}"
    
    @property
    def pontuacao_ponderada(self):
        return self.pontuacao * self.peso * 10

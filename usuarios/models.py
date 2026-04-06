from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator


class Usuario(AbstractUser):
    PERFIL_CHOICES = [
        ('DEMANDANTE', 'Demandante'),
        ('SUPRN', 'SUPRN'),
        ('GERENTE_PROJETO', 'Gerente de Projeto'),
        ('GERENTE_PORTFOLIO', 'Gerente de Portfólio'),
        ('COORDENADOR', 'Coordenador'),
        ('PRESIDENCIA', 'Presidência'),
    ]
    
    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='DEMANDANTE',
        db_index=True
    )
    setor = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    matricula = models.CharField(max_length=20, unique=True, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['perfil', 'ativo']),
            models.Index(fields=['matricula']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_perfil_display()})"
    
    def tem_permissao(self, acao):
        permissoes = {
            'DEMANDANTE': ['submeter_projeto', 'visualizar_proprio_projeto'],
            'SUPRN': ['avaliar_projeto', 'visualizar_projetos'],
            'GERENTE_PROJETO': ['gerenciar_projeto', 'atualizar_status'],
            'GERENTE_PORTFOLIO': ['priorizar_projeto', 'consolidar_carteira'],
            'COORDENADOR': ['validar_carteira', 'aprovar_projeto'],
            'PRESIDENCIA': ['deliberar_projeto', 'aprovar_final'],
        }
        return acao in permissoes.get(self.perfil, [])

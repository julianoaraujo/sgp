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


class PhasePermission(models.Model):
    """Mapa configurável de quais perfis executam cada fase do fluxo"""

    PHASE_CHOICES = [
        ('AVALIACAO', 'Avaliação'),
        ('VIABILIDADE', 'Viabilidade'),
        ('PRIORIZACAO', 'Priorização'),
        ('CONSOLIDACAO', 'Consolidação / adicionar projetos'),
        ('VALIDACAO', 'Validação de carteira'),
        ('DELIBERACAO', 'Deliberação da carteira'),
    ]

    phase = models.CharField(max_length=20, choices=PHASE_CHOICES, unique=True)
    allowed_perfis = models.CharField(
        max_length=200,
        help_text='Perfis permitidos separados por vírgula. Ex: SUPRN,GERENTE_PORTFOLIO'
    )

    class Meta:
        db_table = 'phase_permissions'
        verbose_name = 'Permissão de Fase'
        verbose_name_plural = 'Permissões de Fase'

    def __str__(self):
        return f"{self.get_phase_display()} -> {self.allowed_perfis}"

    @property
    def perfis_list(self):
        return [p.strip() for p in self.allowed_perfis.split(',') if p.strip()]


DEFAULT_PHASE_PERFIS = {
    'AVALIACAO': ['SUPRN'],
    'VIABILIDADE': ['SUPRN', 'GERENTE_PORTFOLIO'],
    'PRIORIZACAO': ['GERENTE_PORTFOLIO', 'COORDENADOR', 'PRESIDENCIA'],
    'CONSOLIDACAO': ['GERENTE_PORTFOLIO'],
    'VALIDACAO': ['COORDENADOR'],
    'DELIBERACAO': ['PRESIDENCIA'],
}


def perfil_pode_fase(usuario, phase_key):
    """Retorna True se o perfil do usuário está autorizado para a fase.
    Busca configuração em PhasePermission; se não existir, usa defaults.
    Superuser sempre pode.
    """
    if not usuario.is_authenticated:
        return False
    if usuario.is_superuser:
        return True

    try:
        perm = PhasePermission.objects.get(phase=phase_key)
        allowed = perm.perfis_list
    except PhasePermission.DoesNotExist:
        allowed = DEFAULT_PHASE_PERFIS.get(phase_key, [])

    return usuario.perfil in allowed

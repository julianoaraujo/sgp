"""
Context processors para adicionar variáveis globais aos templates
"""
from .models import Notificacao


def notificacoes_nao_lidas(request):
    """
    Adiciona o contador de notificações não lidas em todos os templates
    """
    if request.user.is_authenticated:
        count = Notificacao.objects.filter(
            destinatario=request.user,
            status='NAO_LIDA'
        ).count()
        return {'notificacoes_nao_lidas': count}
    return {'notificacoes_nao_lidas': 0}

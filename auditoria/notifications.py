"""
Sistema de notificações automáticas
"""
from auditoria.models import Notificacao
from usuarios.models import Usuario


def notificar_usuarios(destinatarios, titulo, mensagem, tipo='INFO', link=None):
    """
    Cria notificações para múltiplos usuários
    """
    notificacoes = []
    for destinatario in destinatarios:
        notificacao = Notificacao.objects.create(
            destinatario=destinatario,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            link=link
        )
        notificacoes.append(notificacao)
    return notificacoes


def notificar_projeto_submetido(projeto):
    """
    Notifica SUPRN quando um projeto é submetido
    """
    suprn_users = Usuario.objects.filter(perfil='SUPRN', is_active=True)
    
    return notificar_usuarios(
        destinatarios=suprn_users,
        titulo=f'Novo projeto submetido: {projeto.titulo}',
        mensagem=f'O projeto "{projeto.titulo}" foi submetido por {projeto.demandante.get_full_name()} e aguarda avaliação.',
        tipo='ALERTA',
        link=f'/projetos/{projeto.id}/'
    )


def notificar_avaliacao_concluida(avaliacao):
    """
    Notifica demandante e gerentes quando avaliação é concluída
    """
    projeto = avaliacao.projeto
    destinatarios = [projeto.demandante]
    
    # Adicionar gerentes de portfólio
    gerentes = Usuario.objects.filter(
        perfil__in=['GERENTE_PORTFOLIO', 'COORDENADOR'],
        is_active=True
    )
    destinatarios.extend(gerentes)
    
    return notificar_usuarios(
        destinatarios=destinatarios,
        titulo=f'Avaliação concluída: {projeto.titulo}',
        mensagem=f'A avaliação do projeto "{projeto.titulo}" foi concluída por {avaliacao.avaliador.get_full_name()}. Pontuação: {avaliacao.pontuacao_parcial}/50.',
        tipo='INFO',
        link=f'/avaliacoes/{avaliacao.id}/'
    )


def notificar_viabilidade_concluida(viabilidade):
    """
    Notifica quando análise de viabilidade é concluída
    """
    projeto = viabilidade.projeto
    destinatarios = [projeto.demandante]
    
    if viabilidade.resultado in ['VIAVEL', 'VIAVEL_COM_RESTRICOES']:
        # Notificar gerentes de portfólio para priorização
        gerentes = Usuario.objects.filter(
            perfil__in=['GERENTE_PORTFOLIO', 'COORDENADOR'],
            is_active=True
        )
        destinatarios.extend(gerentes)
        
        tipo = 'ALERTA'
        titulo = f'Projeto viável: {projeto.titulo}'
        mensagem = f'O projeto "{projeto.titulo}" foi considerado {viabilidade.get_resultado_display()} e está pronto para priorização.'
    else:
        tipo = 'URGENTE'
        titulo = f'Projeto inviável: {projeto.titulo}'
        mensagem = f'O projeto "{projeto.titulo}" foi considerado inviável e foi rejeitado.'
    
    return notificar_usuarios(
        destinatarios=destinatarios,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,
        link=f'/projetos/{projeto.id}/'
    )


def notificar_priorizacao_concluida(priorizacao):
    """
    Notifica quando priorização é concluída
    """
    projeto = priorizacao.projeto
    destinatarios = [projeto.demandante]
    
    # Notificar coordenadores
    coordenadores = Usuario.objects.filter(
        perfil__in=['COORDENADOR', 'PRESIDENCIA'],
        is_active=True
    )
    destinatarios.extend(coordenadores)
    
    return notificar_usuarios(
        destinatarios=destinatarios,
        titulo=f'Priorização concluída: {projeto.titulo}',
        mensagem=f'O projeto "{projeto.titulo}" foi priorizado com pontuação total de {projeto.pontuacao_total} pontos.',
        tipo='INFO',
        link=f'/projetos/{projeto.id}/'
    )


def notificar_carteira_criada(carteira):
    """
    Notifica quando uma carteira é criada
    """
    coordenadores = Usuario.objects.filter(
        perfil__in=['COORDENADOR', 'PRESIDENCIA'],
        is_active=True
    )
    
    return notificar_usuarios(
        destinatarios=coordenadores,
        titulo=f'Nova carteira criada: {carteira.titulo}',
        mensagem=f'A carteira "{carteira.titulo}" ({carteira.ano}/{carteira.periodo}) foi criada e aguarda validação.',
        tipo='ALERTA',
        link=f'/carteiras/{carteira.id}/'
    )


def notificar_carteira_validada(carteira):
    """
    Notifica quando carteira é validada
    """
    presidencia = Usuario.objects.filter(perfil='PRESIDENCIA', is_active=True)
    
    return notificar_usuarios(
        destinatarios=presidencia,
        titulo=f'Carteira validada: {carteira.titulo}',
        mensagem=f'A carteira "{carteira.titulo}" foi validada e aguarda deliberação da presidência.',
        tipo='URGENTE',
        link=f'/carteiras/{carteira.id}/'
    )


def notificar_projeto_aprovado(projeto):
    """
    Notifica quando projeto é aprovado
    """
    destinatarios = [projeto.demandante]
    
    # Adicionar gerente do projeto se houver
    if projeto.gerente:
        destinatarios.append(projeto.gerente)
    
    return notificar_usuarios(
        destinatarios=destinatarios,
        titulo=f'Projeto aprovado: {projeto.titulo}',
        mensagem=f'Parabéns! O projeto "{projeto.titulo}" foi aprovado e está pronto para execução.',
        tipo='INFO',
        link=f'/projetos/{projeto.id}/'
    )


def notificar_projeto_rejeitado(projeto, motivo=''):
    """
    Notifica quando projeto é rejeitado
    """
    mensagem = f'O projeto "{projeto.titulo}" foi rejeitado.'
    if motivo:
        mensagem += f' Motivo: {motivo}'
    
    return notificar_usuarios(
        destinatarios=[projeto.demandante],
        titulo=f'Projeto rejeitado: {projeto.titulo}',
        mensagem=mensagem,
        tipo='URGENTE',
        link=f'/projetos/{projeto.id}/'
    )


def notificar_mudanca_status(projeto, status_anterior, status_novo):
    """
    Notifica mudança de status do projeto
    """
    return notificar_usuarios(
        destinatarios=[projeto.demandante],
        titulo=f'Status alterado: {projeto.titulo}',
        mensagem=f'O status do projeto "{projeto.titulo}" mudou de {status_anterior} para {status_novo}.',
        tipo='INFO',
        link=f'/projetos/{projeto.id}/'
    )

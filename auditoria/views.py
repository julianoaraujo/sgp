from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Notificacao


@login_required
def notificacao_list(request):
    """Lista todas as notificações do usuário"""
    notificacoes = Notificacao.objects.filter(
        destinatario=request.user
    ).order_by('-data_criacao')
    
    # Filtros
    status = request.GET.get('status')
    if status:
        notificacoes = notificacoes.filter(status=status)
    
    tipo = request.GET.get('tipo')
    if tipo:
        notificacoes = notificacoes.filter(tipo=tipo)
    
    # Paginação
    paginator = Paginator(notificacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total = notificacoes.count()
    nao_lidas = notificacoes.filter(status='NAO_LIDA').count()
    
    context = {
        'notificacoes': page_obj,
        'total_notificacoes': total,
        'notificacoes_nao_lidas': nao_lidas,
    }
    
    return render(request, 'notificacao_list.html', context)


@login_required
def notificacao_marcar_lida(request, pk):
    """Marca uma notificação como lida"""
    notificacao = get_object_or_404(Notificacao, pk=pk, destinatario=request.user)
    notificacao.status = 'LIDA'
    notificacao.save()
    
    # Se tem link, redireciona para ele
    if notificacao.link:
        return redirect(notificacao.link)
    
    return redirect('notificacao_list')


@login_required
def notificacao_marcar_todas_lidas(request):
    """Marca todas as notificações como lidas"""
    Notificacao.objects.filter(
        destinatario=request.user,
        status='NAO_LIDA'
    ).update(status='LIDA')
    
    messages.success(request, 'Todas as notificações foram marcadas como lidas.')
    return redirect('notificacao_list')


@login_required
def notificacao_arquivar(request, pk):
    """Arquiva uma notificação"""
    notificacao = get_object_or_404(Notificacao, pk=pk, destinatario=request.user)
    notificacao.status = 'ARQUIVADA'
    notificacao.save()
    
    messages.success(request, 'Notificação arquivada.')
    return redirect('notificacao_list')


@login_required
def notificacao_deletar(request, pk):
    """Deleta uma notificação"""
    notificacao = get_object_or_404(Notificacao, pk=pk, destinatario=request.user)
    notificacao.delete()
    
    messages.success(request, 'Notificação excluída.')
    return redirect('notificacao_list')

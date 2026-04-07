from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Projeto
from auditoria.models import Notificacao


@login_required
def dashboard(request):
    total_projetos = Projeto.objects.filter(ativo=True).count()
    projetos_aceitos = Projeto.objects.filter(status='ACEITO', ativo=True).count()
    projetos_em_avaliacao = Projeto.objects.filter(
        status__in=['EM_AVALIACAO', 'EM_VIABILIDADE', 'EM_PRIORIZACAO'],
        ativo=True
    ).count()
    
    from carteira.models import Carteira
    carteiras_ativas = Carteira.objects.filter(
        status__in=['EM_CONSOLIDACAO', 'EM_VALIDACAO', 'EM_DELIBERACAO']
    ).count()
    
    if request.user.perfil == 'DEMANDANTE':
        projetos_recentes = Projeto.objects.filter(
            demandante=request.user,
            ativo=True
        ).order_by('-data_criacao')[:5]
    else:
        projetos_recentes = Projeto.objects.filter(
            ativo=True
        ).order_by('-data_criacao')[:5]
    
    notificacoes = Notificacao.objects.filter(
        destinatario=request.user,
        status='NAO_LIDA'
    ).order_by('-data_criacao')[:5]
    
    context = {
        'total_projetos': total_projetos,
        'projetos_aceitos': projetos_aceitos,
        'projetos_em_avaliacao': projetos_em_avaliacao,
        'carteiras_ativas': carteiras_ativas,
        'projetos_recentes': projetos_recentes,
        'notificacoes': notificacoes,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def projeto_list(request):
    projetos = Projeto.objects.filter(ativo=True)
    
    if request.user.perfil == 'DEMANDANTE':
        projetos = projetos.filter(demandante=request.user)
    
    q = request.GET.get('q')
    if q:
        projetos = projetos.filter(
            Q(titulo__icontains=q) | Q(descricao__icontains=q)
        )
    
    status = request.GET.get('status')
    if status:
        projetos = projetos.filter(status=status)
    
    prioridade = request.GET.get('prioridade')
    if prioridade:
        projetos = projetos.filter(prioridade=prioridade)
    
    projetos = projetos.order_by('-data_criacao')
    
    paginator = Paginator(projetos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'projeto_list.html', {'projetos': page_obj})


@login_required
def projeto_detail(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk, ativo=True)
    
    if request.user.perfil == 'DEMANDANTE' and projeto.demandante != request.user:
        messages.error(request, 'Você não tem permissão para visualizar este projeto.')
        return redirect('projeto_list')
    
    return render(request, 'projeto_detail.html', {'projeto': projeto})


@login_required
def projeto_create(request):
    if request.user.perfil not in ['DEMANDANTE', 'PRESIDENCIA'] and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para criar projetos.')
        return redirect('projeto_list')
    
    if request.method == 'POST':
        projeto = Projeto.objects.create(
            titulo=request.POST.get('titulo'),
            descricao=request.POST.get('descricao'),
            justificativa=request.POST.get('justificativa'),
            objetivos=request.POST.get('objetivos'),
            resultados_esperados=request.POST.get('resultados_esperados'),
            demandante=request.user,
            status='RASCUNHO'
        )
        messages.success(request, 'Projeto criado com sucesso!')
        return redirect('projeto_detail', pk=projeto.pk)
    
    return render(request, 'projeto_form.html')


@login_required
def projeto_edit(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk, ativo=True)
    
    if projeto.demandante != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este projeto.')
        return redirect('projeto_list')
    
    if request.method == 'POST':
        projeto.titulo = request.POST.get('titulo')
        projeto.descricao = request.POST.get('descricao')
        projeto.justificativa = request.POST.get('justificativa')
        projeto.objetivos = request.POST.get('objetivos')
        projeto.resultados_esperados = request.POST.get('resultados_esperados')
        projeto.save()
        
        messages.success(request, 'Projeto atualizado com sucesso!')
        return redirect('projeto_detail', pk=projeto.pk)
    
    return render(request, 'projeto_form.html', {'projeto': projeto})


@login_required
def projeto_submeter(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk, ativo=True)
    
    if projeto.demandante != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para submeter este projeto.')
        return redirect('projeto_list')
    
    if projeto.status != 'RASCUNHO':
        messages.warning(request, 'Este projeto já foi submetido.')
        return redirect('projeto_detail', pk=projeto.pk)
    
    if not projeto.pode_transicionar_para('SUBMETIDO'):
        messages.error(request, 'Este projeto não pode ser submetido no momento.')
        return redirect('projeto_detail', pk=projeto.pk)
    
    projeto.status = 'SUBMETIDO'
    projeto.data_submissao = timezone.now()
    projeto.save()
    
    messages.success(request, 'Projeto submetido com sucesso! Aguardando avaliação.')
    return redirect('projeto_detail', pk=projeto.pk)


@login_required
def perfil(request):
    return render(request, 'perfil.html')

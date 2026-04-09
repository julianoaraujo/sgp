from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal
from .models import Avaliacao, Viabilidade, Priorizacao
from projetos.models import Projeto
from auditoria.notifications import (
    notificar_avaliacao_concluida,
    notificar_viabilidade_concluida,
    notificar_priorizacao_concluida
)
from usuarios.models import perfil_pode_fase


@login_required
def avaliacao_list(request):
    if request.user.perfil not in ['SUPRN', 'GERENTE_PORTFOLIO', 'COORDENADOR', 'PRESIDENCIA']:
        messages.error(request, 'Você não tem permissão para acessar avaliações.')
        return redirect('dashboard')
    
    avaliacoes = Avaliacao.objects.all().select_related('projeto', 'avaliador')
    
    if request.user.perfil == 'SUPRN':
        avaliacoes = avaliacoes.filter(avaliador=request.user)
    
    q = request.GET.get('q')
    if q:
        avaliacoes = avaliacoes.filter(
            Q(projeto__titulo__icontains=q) | Q(parecer_tecnico__icontains=q)
        )
    
    status = request.GET.get('status')
    if status:
        avaliacoes = avaliacoes.filter(status=status)
    
    avaliacoes = avaliacoes.order_by('-data_inicio')
    
    paginator = Paginator(avaliacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'avaliacoes': page_obj,
        'total_avaliacoes': avaliacoes.count(),
        'avaliacoes_pendentes': avaliacoes.filter(status='PENDENTE').count(),
        'avaliacoes_concluidas': avaliacoes.filter(status='CONCLUIDA').count(),
    }
    
    return render(request, 'avaliacao_list.html', context)


@login_required
def avaliacao_detail(request, pk):
    avaliacao = get_object_or_404(Avaliacao, pk=pk)
    
    if request.user.perfil == 'SUPRN' and avaliacao.avaliador != request.user:
        messages.error(request, 'Você não tem permissão para visualizar esta avaliação.')
        return redirect('avaliacao_list')
    
    return render(request, 'avaliacao_detail.html', {'avaliacao': avaliacao})


@login_required
def avaliacao_create(request, projeto_id):
    if not perfil_pode_fase(request.user, 'AVALIACAO'):
        messages.error(request, 'Você não tem permissão para criar avaliações.')
        return redirect('projeto_detail', pk=projeto_id)
    
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    
    if projeto.status not in ['SUBMETIDO', 'EM_AVALIACAO']:
        messages.error(request, 'Este projeto não está disponível para avaliação.')
        return redirect('projeto_detail', pk=projeto_id)
    
    if Avaliacao.objects.filter(projeto=projeto, avaliador=request.user).exists():
        messages.warning(request, 'Você já avaliou este projeto.')
        return redirect('projeto_detail', pk=projeto_id)
    
    if request.method == 'POST':
        try:
            pontuacao_a = Decimal(request.POST.get('pontuacao_etapa_a', 0))
            pontuacao_b = Decimal(request.POST.get('pontuacao_etapa_b', 0))
            
            if pontuacao_a < 0 or pontuacao_a > 25:
                messages.error(request, 'Pontuação da Etapa A deve estar entre 0 e 25.')
                return render(request, 'avaliacao_form.html', {'projeto': projeto})
            
            if pontuacao_b < 0 or pontuacao_b > 25:
                messages.error(request, 'Pontuação da Etapa B deve estar entre 0 e 25.')
                return render(request, 'avaliacao_form.html', {'projeto': projeto})
            
            avaliacao = Avaliacao.objects.create(
                projeto=projeto,
                avaliador=request.user,
                pontuacao_etapa_a=pontuacao_a,
                pontuacao_etapa_b=pontuacao_b,
                parecer_tecnico=request.POST.get('parecer_tecnico'),
                recomendacoes=request.POST.get('recomendacoes', ''),
                status='CONCLUIDA'
            )
            
            if projeto.status == 'SUBMETIDO':
                projeto.status = 'EM_AVALIACAO'
                projeto.save()
            
            # Notificar demandante e gerentes
            notificar_avaliacao_concluida(avaliacao)
            
            messages.success(request, 'Avaliação criada com sucesso!')
            return redirect('avaliacao_detail', pk=avaliacao.pk)
            
        except Exception as e:
            messages.error(request, f'Erro ao criar avaliação: {str(e)}')
    
    return render(request, 'avaliacao_form.html', {'projeto': projeto})


@login_required
def viabilidade_create(request, projeto_id):
    if not perfil_pode_fase(request.user, 'VIABILIDADE'):
        messages.error(request, 'Você não tem permissão para analisar viabilidade.')
        return redirect('projeto_detail', pk=projeto_id)
    
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    
    if projeto.status not in ['EM_AVALIACAO', 'EM_VIABILIDADE']:
        messages.error(request, 'Este projeto não está disponível para análise de viabilidade.')
        return redirect('projeto_detail', pk=projeto_id)
    
    if request.method == 'POST':
        try:
            resultado = request.POST.get('resultado')
            
            viabilidade = Viabilidade.objects.create(
                projeto=projeto,
                analista=request.user,
                viabilidade_tecnica=request.POST.get('viabilidade_tecnica') == 'True',
                viabilidade_financeira=request.POST.get('viabilidade_financeira') == 'True',
                viabilidade_operacional=request.POST.get('viabilidade_operacional') == 'True',
                viabilidade_juridica=request.POST.get('viabilidade_juridica') == 'True',
                analise_tecnica=request.POST.get('analise_tecnica', ''),
                analise_financeira=request.POST.get('analise_financeira', ''),
                analise_operacional=request.POST.get('analise_operacional', ''),
                analise_juridica=request.POST.get('analise_juridica', ''),
                resultado=resultado,
                riscos_identificados=request.POST.get('riscos_identificados', ''),
                restricoes=request.POST.get('restricoes', ''),
                status='CONCLUIDA'
            )
            
            # Atualizar status do projeto baseado no resultado da viabilidade
            if resultado == 'VIAVEL' or resultado == 'VIAVEL_COM_RESTRICOES':
                projeto.status = 'EM_PRIORIZACAO'
                messages.success(request, 'Análise de viabilidade concluída! Projeto aprovado para priorização.')
            else:
                projeto.status = 'REJEITADO'
                messages.warning(request, 'Projeto considerado inviável e foi rejeitado.')
            
            projeto.save()
            
            # Notificar demandante e gerentes
            notificar_viabilidade_concluida(viabilidade)
            
            return redirect('projeto_detail', pk=projeto.pk)
            
        except Exception as e:
            messages.error(request, f'Erro ao criar análise: {str(e)}')
    
    return render(request, 'viabilidade_form.html', {'projeto': projeto})


@login_required
def priorizacao_create(request, projeto_id):
    if not perfil_pode_fase(request.user, 'PRIORIZACAO'):
        messages.error(request, 'Você não tem permissão para priorizar projetos.')
        return redirect('projeto_detail', pk=projeto_id)
    
    projeto = get_object_or_404(Projeto, pk=projeto_id)
    
    if projeto.status not in ['EM_VIABILIDADE', 'EM_PRIORIZACAO']:
        messages.error(request, 'Este projeto não está disponível para priorização.')
        return redirect('projeto_detail', pk=projeto_id)
    
    avaliacao = Avaliacao.objects.filter(projeto=projeto, status='CONCLUIDA').first()
    
    if request.method == 'POST':
        try:
            pontuacao_c = Decimal(request.POST.get('pontuacao_etapa_c', 0))
            
            if pontuacao_c < 0 or pontuacao_c > 60:
                messages.error(request, 'Pontuação da Etapa C deve estar entre 0 e 60.')
                return render(request, 'priorizacao_form.html', {
                    'projeto': projeto,
                    'avaliacao': avaliacao
                })
            
            priorizacao = Priorizacao.objects.create(
                projeto=projeto,
                responsavel=request.user,
                pontuacao_etapa_c=pontuacao_c,
                complexidade=int(request.POST.get('complexidade')),
                urgencia=int(request.POST.get('urgencia')),
                impacto_estrategico=int(request.POST.get('impacto_estrategico')),
                recursos_disponiveis=request.POST.get('recursos_disponiveis') == 'True',
                dependencias_externas=request.POST.get('dependencias_externas') == 'True',
                justificativa=request.POST.get('justificativa'),
                observacoes=request.POST.get('observacoes', '')
            )
            
            pontuacao_total = pontuacao_c
            if avaliacao:
                pontuacao_total += avaliacao.pontuacao_parcial
            
            projeto.pontuacao_total = pontuacao_total
            projeto.status = 'PRIORIZADO'
            projeto.save()
            
            # Notificar demandante e coordenadores
            notificar_priorizacao_concluida(priorizacao)
            
            messages.success(request, f'Priorização criada com sucesso! Pontuação total: {pontuacao_total}. Projeto priorizado e pronto para consolidação em carteira.')
            return redirect('projeto_detail', pk=projeto.pk)
            
        except Exception as e:
            messages.error(request, f'Erro ao criar priorização: {str(e)}')
    
    return render(request, 'priorizacao_form.html', {
        'projeto': projeto,
        'avaliacao': avaliacao
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.utils import timezone
from decimal import Decimal
from django.db import IntegrityError
from .models import Carteira, ProjetoCarteira, Validacao
from usuarios.models import perfil_pode_fase
from projetos.models import Projeto
from auditoria.notifications import notificar_carteira_criada, notificar_carteira_validada


@login_required
def carteira_list(request):
    """Lista todas as carteiras"""
    if request.user.perfil not in ['GERENTE_PORTFOLIO', 'COORDENADOR', 'PRESIDENCIA']:
        messages.error(request, 'Você não tem permissão para acessar carteiras.')
        return redirect('dashboard')
    
    carteiras = Carteira.objects.all().select_related('gerente_portfolio').annotate(
        total_projetos=Count('projetos'),
        orcamento_projetos=Sum('projetos__projeto__orcamento_previsto')
    )
    
    # Filtros
    ano = request.GET.get('ano')
    if ano:
        carteiras = carteiras.filter(ano=ano)
    
    status = request.GET.get('status')
    if status:
        carteiras = carteiras.filter(status=status)
    
    q = request.GET.get('q')
    if q:
        carteiras = carteiras.filter(
            Q(nome__icontains=q) | Q(descricao__icontains=q)
        )
    
    carteiras = carteiras.order_by('-ano', '-data_criacao')
    
    # Paginação
    paginator = Paginator(carteiras, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_carteiras = carteiras.count()
    em_consolidacao = carteiras.filter(status='EM_CONSOLIDACAO').count()
    validadas = carteiras.filter(status='VALIDADA').count()
    aprovadas = carteiras.filter(status='APROVADA').count()
    
    # Anos disponíveis
    anos_disponiveis = Carteira.objects.values_list('ano', flat=True).distinct().order_by('-ano')
    
    context = {
        'carteiras': page_obj,
        'total_carteiras': total_carteiras,
        'em_consolidacao': em_consolidacao,
        'validadas': validadas,
        'aprovadas': aprovadas,
        'anos_disponiveis': anos_disponiveis,
    }
    
    return render(request, 'carteira_list.html', context)


@login_required
def carteira_detail(request, pk):
    """Detalhes da carteira com projetos e análises"""
    carteira = get_object_or_404(Carteira, pk=pk)
    
    if request.user.perfil not in ['GERENTE_PORTFOLIO', 'COORDENADOR', 'PRESIDENCIA']:
        messages.error(request, 'Você não tem permissão para visualizar esta carteira.')
        return redirect('carteira_list')
    
    # Projetos da carteira ordenados por pontuação
    projetos_carteira = carteira.projetos.all().select_related(
        'projeto', 'projeto__demandante'
    ).order_by('-projeto__pontuacao_total')
    
    # Estatísticas da carteira
    stats = {
        'total_projetos': projetos_carteira.count(),
        'orcamento_total': projetos_carteira.aggregate(
            total=Sum('projeto__orcamento_previsto')
        )['total'] or Decimal('0.00'),
        'pontuacao_media': projetos_carteira.aggregate(
            media=Avg('projeto__pontuacao_total')
        )['media'] or Decimal('0.00'),
        'projetos_alta_prioridade': projetos_carteira.filter(
            projeto__pontuacao_total__gte=80
        ).count(),
        'projetos_incluidos': projetos_carteira.filter(incluido_carteira=True).count(),
        'projetos_excluidos': projetos_carteira.filter(incluido_carteira=False).count(),
    }
    
    # Validações da carteira
    validacoes = Validacao.objects.filter(
        carteira=carteira
    ).select_related('validador').order_by('-data_inicio')
    
    context = {
        'carteira': carteira,
        'projetos_carteira': projetos_carteira,
        'stats': stats,
        'validacoes': validacoes,
    }
    
    return render(request, 'carteira_detail.html', context)


@login_required
def carteira_create(request):
    """Cria nova carteira"""
    if request.user.perfil not in ['GERENTE_PORTFOLIO']:
        messages.error(request, 'Apenas Gerentes de Portfólio podem criar carteiras.')
        return redirect('carteira_list')
    
    if request.method == 'POST':
        try:
            # Criar carteira (campos alinhados ao formulário)
            # Sanitiza orçamento: remove separador de milhar e converte vírgula em ponto
            raw_orcamento = (request.POST.get('orcamento_total', '') or '').replace('.', '').replace(',', '.')
            # Validação de unicidade ano/período
            ano = int(request.POST.get('ano'))
            periodo = request.POST.get('periodo')
            if Carteira.objects.filter(ano=ano, periodo=periodo).exists():
                messages.error(request, 'Já existe uma carteira para este ano e período.')
                return render(request, 'carteira_form.html', {
                    'ano_atual': timezone.now().year,
                    'erro_unicidade': True
                })

            carteira = Carteira.objects.create(
                titulo=request.POST.get('titulo'),
                descricao=request.POST.get('descricao'),
                ano=ano,
                periodo=periodo,
                orcamento_total=Decimal(raw_orcamento or '0'),
                gerente_portfolio=request.user,
                status='EM_CONSOLIDACAO'
            )
            
            # Notificar coordenadores
            notificar_carteira_criada(carteira)
            
            messages.success(request, f'Carteira "{carteira.titulo}" criada com sucesso!')
            return redirect('carteira_detail', pk=carteira.pk)
            
        except IntegrityError:
            messages.error(request, 'Já existe uma carteira para este ano e período.')
        except Exception as e:
            messages.error(request, f'Erro ao criar carteira: {str(e)}')
    
    # Projetos priorizados disponíveis para adicionar à carteira
    projetos_disponiveis = Projeto.objects.filter(
        status='PRIORIZADO',
        ativo=True
    ).exclude(
        carteiras__isnull=False
    ).order_by('-pontuacao_total')
    
    context = {
        'projetos_disponiveis': projetos_disponiveis,
        'ano_atual': timezone.now().year,
    }
    
    return render(request, 'carteira_form.html', context)


@login_required
def carteira_adicionar_projeto(request, pk):
    """Adiciona projeto à carteira"""
    if not perfil_pode_fase(request.user, 'CONSOLIDACAO'):
        messages.error(request, 'Você não tem permissão para adicionar projetos nesta fase.')
        return redirect('carteira_detail', pk=pk)
    
    carteira = get_object_or_404(Carteira, pk=pk)
    
    if carteira.status not in ['EM_CONSOLIDACAO']:
        messages.error(request, 'Não é possível adicionar projetos a esta carteira.')
        return redirect('carteira_detail', pk=pk)
    
    if request.method == 'POST':
        projeto_ids = request.POST.getlist('projetos')
        
        for projeto_id in projeto_ids:
            projeto = get_object_or_404(Projeto, pk=projeto_id)
            
            # Verificar se projeto já está em outra carteira
            if ProjetoCarteira.objects.filter(projeto=projeto).exists():
                messages.warning(request, f'Projeto "{projeto.titulo}" já está em outra carteira.')
                continue
            
            # Adicionar à carteira
            ProjetoCarteira.objects.create(
                carteira=carteira,
                projeto=projeto,
                posicao_ranking=ProjetoCarteira.objects.filter(carteira=carteira).count() + 1
            )
        
        messages.success(request, f'{len(projeto_ids)} projeto(s) adicionado(s) à carteira.')
        return redirect('carteira_detail', pk=carteira.pk)
    
    # Projetos disponíveis
    projetos_disponiveis = Projeto.objects.filter(
        status='PRIORIZADO',
        ativo=True
    ).exclude(
        carteiras__isnull=False
    ).order_by('-pontuacao_total')
    
    context = {
        'carteira': carteira,
        'projetos_disponiveis': projetos_disponiveis,
    }
    
    return render(request, 'carteira_adicionar_projeto.html', context)


@login_required
def carteira_remover_projeto(request, pk, projeto_id):
    """Remove projeto da carteira"""
    if not perfil_pode_fase(request.user, 'CONSOLIDACAO'):
        messages.error(request, 'Você não tem permissão para remover projetos nesta fase.')
        return redirect('carteira_detail', pk=pk)
    
    carteira = get_object_or_404(Carteira, pk=pk)
    
    if carteira.status not in ['EM_CONSOLIDACAO']:
        messages.error(request, 'Não é possível remover projetos desta carteira.')
        return redirect('carteira_detail', pk=pk)
    
    projeto_carteira = get_object_or_404(
        ProjetoCarteira,
        carteira=carteira,
        projeto_id=projeto_id
    )
    
    projeto_titulo = projeto_carteira.projeto.titulo
    projeto_carteira.delete()
    
    messages.success(request, f'Projeto "{projeto_titulo}" removido da carteira.')
    return redirect('carteira_detail', pk=pk)


@login_required
def carteira_validar(request, pk):
    """Validação da carteira pelo coordenador"""
    if not perfil_pode_fase(request.user, 'VALIDACAO'):
        messages.error(request, 'Você não tem permissão para validar carteiras.')
        return redirect('carteira_detail', pk=pk)
    
    carteira = get_object_or_404(Carteira, pk=pk)
    
    if carteira.status != 'EM_CONSOLIDACAO':
        messages.error(request, 'Esta carteira não está disponível para validação.')
        return redirect('carteira_detail', pk=pk)
    
    if request.method == 'POST':
        aprovado = request.POST.get('aprovado') == 'True'
        
        # Criar validação
        validacao = Validacao.objects.create(
            carteira=carteira,
            validador=request.user,
            status='APROVADA' if aprovado else 'REJEITADA',
            parecer=request.POST.get('observacoes', ''),
            recomendacoes=request.POST.get('recomendacoes', '')
        )
        
        if aprovado:
            carteira.status = 'EM_VALIDACAO'
            carteira.data_validacao = timezone.now()
            carteira.save()
            
            # Notificar presidência
            notificar_carteira_validada(carteira)
            
            messages.success(request, 'Carteira validada com sucesso! Aguardando deliberação da presidência.')
        else:
            carteira.status = 'EM_CONSOLIDACAO'
            carteira.save()
            messages.warning(request, 'Carteira devolvida para ajustes.')
        
        return redirect('carteira_detail', pk=carteira.pk)
    
    context = {
        'carteira': carteira,
    }
    
    return render(request, 'carteira_validacao.html', context)


@login_required
def carteira_deliberar(request, pk):
    """Deliberação final da carteira pela presidência"""
    if not perfil_pode_fase(request.user, 'DELIBERACAO'):
        messages.error(request, 'Você não tem permissão para deliberar sobre carteiras.')
        return redirect('carteira_detail', pk=pk)
    
    carteira = get_object_or_404(Carteira, pk=pk)
    
    if carteira.status != 'EM_VALIDACAO':
        messages.error(request, 'Esta carteira não está disponível para deliberação.')
        return redirect('carteira_detail', pk=pk)
    
    if request.method == 'POST':
        aprovado = request.POST.get('aprovado') == 'True'
        
        if aprovado:
            carteira.status = 'APROVADA'
            carteira.data_aprovacao = timezone.now()
            
            # Atualizar status dos projetos da carteira
            projetos = ProjetoCarteira.objects.filter(carteira=carteira)
            for pc in projetos:
                pc.projeto.status = 'ACEITO'
                pc.projeto.save()
            
            messages.success(request, f'Carteira aprovada! {projetos.count()} projeto(s) aceito(s) para execução.')
        else:
            carteira.status = 'REJEITADA'
            messages.warning(request, 'Carteira rejeitada.')
        
        carteira.observacoes = request.POST.get('observacoes', '')
        carteira.save()
        
        return redirect('carteira_detail', pk=carteira.pk)
    
    context = {
        'carteira': carteira,
    }
    
    return render(request, 'carteira_deliberacao.html', context)

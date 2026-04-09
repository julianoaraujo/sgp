from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import PhasePermission, DEFAULT_PHASE_PERFIS, Usuario


@login_required
def phase_permissions(request):
    if not request.user.is_superuser:
        messages.error(request, 'Apenas superadmins podem configurar o fluxo de negócio.')
        return redirect('dashboard')

    # Garantir que todas as fases existam com default
    for phase, perfis in DEFAULT_PHASE_PERFIS.items():
        PhasePermission.objects.get_or_create(
            phase=phase,
            defaults={'allowed_perfis': ','.join(perfis)}
        )

    phases = PhasePermission.objects.order_by('phase')
    perfis_choices = Usuario.PERFIL_CHOICES

    if request.method == 'POST':
        for phase in phases:
            key = f"perfis_{phase.phase}"
            valores = request.POST.getlist(key)
            phase.allowed_perfis = ','.join(valores)
            phase.save()
        messages.success(request, 'Configuração de fluxo atualizada com sucesso.')
        return redirect('phase_permissions')

    context = {
        'phases': phases,
        'perfis_choices': perfis_choices,
    }
    return render(request, 'phase_permissions.html', context)

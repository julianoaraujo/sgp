from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def carteira_list(request):
    return render(request, 'carteira_list.html', {})

urlpatterns = [
    path('', carteira_list, name='carteira_list'),
]

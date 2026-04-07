"""
Script para criar usuários de teste com diferentes perfis
Execute: python manage.py shell < create_test_users.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgp.settings')
django.setup()

from usuarios.models import Usuario

# Dados dos usuários de teste
usuarios_teste = [
    {
        'username': 'suprn',
        'email': 'suprn@itec.gov.br',
        'first_name': 'Analista',
        'last_name': 'SUPRN',
        'perfil': 'SUPRN',
        'setor': 'SUPRN - Superintendência de Projetos',
        'password': 'suprn123',
    },
    {
        'username': 'demandante',
        'email': 'demandante@itec.gov.br',
        'first_name': 'João',
        'last_name': 'Silva',
        'perfil': 'DEMANDANTE',
        'setor': 'Departamento de TI',
        'password': 'demandante123',
    },
    {
        'username': 'gerente_projeto',
        'email': 'gerente.projeto@itec.gov.br',
        'first_name': 'Maria',
        'last_name': 'Santos',
        'perfil': 'GERENTE_PROJETO',
        'setor': 'Gerência de Projetos',
        'password': 'gerente123',
    },
    {
        'username': 'gerente_portfolio',
        'email': 'gerente.portfolio@itec.gov.br',
        'first_name': 'Carlos',
        'last_name': 'Oliveira',
        'perfil': 'GERENTE_PORTFOLIO',
        'setor': 'Gerência de Portfólio',
        'password': 'portfolio123',
    },
    {
        'username': 'coordenador',
        'email': 'coordenador@itec.gov.br',
        'first_name': 'Ana',
        'last_name': 'Costa',
        'perfil': 'COORDENADOR',
        'setor': 'Coordenação Executiva',
        'password': 'coordenador123',
    },
    {
        'username': 'presidencia',
        'email': 'presidencia@itec.gov.br',
        'first_name': 'Roberto',
        'last_name': 'Almeida',
        'perfil': 'PRESIDENCIA',
        'setor': 'Presidência',
        'password': 'presidencia123',
        'is_staff': True,
    },
]

print("\n" + "="*70)
print("CRIANDO USUÁRIOS DE TESTE")
print("="*70 + "\n")

for dados in usuarios_teste:
    username = dados.pop('username')
    password = dados.pop('password')
    
    if Usuario.objects.filter(username=username).exists():
        print(f"❌ Usuário '{username}' já existe. Pulando...")
        continue
    
    usuario = Usuario.objects.create_user(
        username=username,
        password=password,
        **dados
    )
    
    print(f"✅ Criado: {username} ({usuario.get_perfil_display()})")
    print(f"   Senha: {password}")
    print(f"   Email: {usuario.email}")
    print()

print("="*70)
print("USUÁRIOS CRIADOS COM SUCESSO!")
print("="*70)
print("\nResumo de acessos:")
print("-" * 70)
print("Perfil              | Usuário           | Senha")
print("-" * 70)
print("Superadmin          | jafar             | (senha gerada)")
print("SUPRN               | suprn             | suprn123")
print("Demandante          | demandante        | demandante123")
print("Gerente Projeto     | gerente_projeto   | gerente123")
print("Gerente Portfólio   | gerente_portfolio | portfolio123")
print("Coordenador         | coordenador       | coordenador123")
print("Presidência         | presidencia       | presidencia123")
print("-" * 70)
print("\n✨ Agora você pode testar o fluxo completo do sistema!\n")

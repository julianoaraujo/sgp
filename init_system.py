import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sgp.settings')
django.setup()

from django.contrib.auth import get_user_model
from projetos.models import Projeto
from avaliacoes.models import Avaliacao
from carteira.models import Carteira

Usuario = get_user_model()

def criar_usuarios_exemplo():
    print("Criando usuários de exemplo...")
    
    usuarios = [
        {
            'username': 'demandante1',
            'email': 'demandante@itec.gov.br',
            'password': 'senha123',
            'perfil': 'DEMANDANTE',
            'first_name': 'João',
            'last_name': 'Silva',
            'setor': 'TI'
        },
        {
            'username': 'suprn1',
            'email': 'suprn@itec.gov.br',
            'password': 'senha123',
            'perfil': 'SUPRN',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'setor': 'SUPRN'
        },
        {
            'username': 'gerente_portfolio1',
            'email': 'gportfolio@itec.gov.br',
            'password': 'senha123',
            'perfil': 'GERENTE_PORTFOLIO',
            'first_name': 'Carlos',
            'last_name': 'Oliveira',
            'setor': 'Gestão'
        },
        {
            'username': 'coordenador1',
            'email': 'coordenador@itec.gov.br',
            'password': 'senha123',
            'perfil': 'COORDENADOR',
            'first_name': 'Ana',
            'last_name': 'Costa',
            'setor': 'Coordenação'
        },
        {
            'username': 'presidencia1',
            'email': 'presidencia@itec.gov.br',
            'password': 'senha123',
            'perfil': 'PRESIDENCIA',
            'first_name': 'Roberto',
            'last_name': 'Almeida',
            'setor': 'Presidência'
        }
    ]
    
    for user_data in usuarios:
        if not Usuario.objects.filter(username=user_data['username']).exists():
            password = user_data.pop('password')
            user = Usuario.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            print(f"✓ Usuário {user.username} criado com sucesso")
        else:
            print(f"- Usuário {user_data['username']} já existe")

def criar_diretorios():
    print("\nCriando diretórios necessários...")
    diretorios = ['logs', 'media', 'staticfiles', 'media/projetos/documentos']
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        print(f"✓ Diretório {diretorio} criado/verificado")

if __name__ == '__main__':
    print("=" * 60)
    print("INICIALIZAÇÃO DO SISTEMA SGP")
    print("=" * 60)
    
    criar_diretorios()
    criar_usuarios_exemplo()
    
    print("\n" + "=" * 60)
    print("SISTEMA INICIALIZADO COM SUCESSO!")
    print("=" * 60)
    print("\nCredenciais de acesso:")
    print("- demandante1 / senha123")
    print("- suprn1 / senha123")
    print("- gerente_portfolio1 / senha123")
    print("- coordenador1 / senha123")
    print("- presidencia1 / senha123")
    print("\nAcesse: http://localhost:8000/admin")

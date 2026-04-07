from django.db import migrations
import secrets
import string


def create_superuser(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    
    if not Usuario.objects.filter(username='jafar').exists():
        chars = string.ascii_letters + string.digits + string.punctuation
        senha_aleatoria = ''.join(secrets.choice(chars) for _ in range(20))
        
        superuser = Usuario.objects.create(
            username='jafar',
            email='jafar@itec.gov.br',
            first_name='Jafar',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
            perfil='PRESIDENCIA',
            setor='TI',
            ativo=True
        )
        superuser.set_password(senha_aleatoria)
        superuser.save()
        
        print("\n" + "="*70)
        print("SUPERUSUÁRIO CRIADO COM SUCESSO!")
        print("="*70)
        print(f"Usuário: jafar")
        print(f"Senha: {senha_aleatoria}")
        print("="*70)
        print("IMPORTANTE: Salve esta senha em local seguro!")
        print("="*70 + "\n")


def reverse_superuser(apps, schema_editor):
    Usuario = apps.get_model('usuarios', 'Usuario')
    Usuario.objects.filter(username='jafar').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, reverse_superuser),
    ]

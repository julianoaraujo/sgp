# Comandos para Iniciar o Sistema SGP

## 🚀 Passo a Passo para Inicialização

### 1. Ativar o Ambiente Virtual

```powershell
# Windows PowerShell
vProjetime26\Scripts\activate
```

### 2. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 3. Criar as Migrações

```powershell
python manage.py makemigrations usuarios
python manage.py makemigrations projetos
python manage.py makemigrations avaliacoes
python manage.py makemigrations carteira
python manage.py makemigrations auditoria
```

### 4. Aplicar as Migrações

```powershell
python manage.py migrate
```

### 5. Criar Diretórios e Usuários de Exemplo

```powershell
python init_system.py
```

**OU** criar apenas um superusuário:

```powershell
python manage.py createsuperuser
```

### 6. Iniciar o Servidor

```powershell
python manage.py runserver
```

### 7. Acessar o Sistema

Abra seu navegador em: **http://localhost:8000/admin**

## 👥 Usuários Criados pelo init_system.py

| Usuário             | Senha    | Perfil              |
|---------------------|----------|---------------------|
| demandante1         | senha123 | Demandante          |
| suprn1              | senha123 | SUPRN               |
| gerente_portfolio1  | senha123 | Gerente Portfólio   |
| coordenador1        | senha123 | Coordenador         |
| presidencia1        | senha123 | Presidência         |

## 🔧 Comandos Úteis

### Verificar Status do Sistema

```powershell
python manage.py check
```

### Verificar Problemas de Deploy

```powershell
python manage.py check --deploy
```

### Criar Backup do Banco

```powershell
python manage.py dumpdata > backup.json
```

### Restaurar Backup

```powershell
python manage.py loaddata backup.json
```

### Limpar Sessões Expiradas

```powershell
python manage.py clearsessions
```

### Acessar Shell Interativo

```powershell
python manage.py shell
```

### Coletar Arquivos Estáticos

```powershell
python manage.py collectstatic --noinput
```

## 🐛 Solução de Problemas Comuns

### Erro: "No module named 'rest_framework'"

```powershell
pip install djangorestframework
```

### Erro: "No module named 'corsheaders'"

```powershell
pip install django-cors-headers
```

### Erro: "No module named 'django_filters'"

```powershell
pip install django-filter
```

### Erro: "Table doesn't exist"

```powershell
python manage.py migrate --run-syncdb
```

### Erro: "CSRF verification failed"

- Limpe os cookies do navegador
- Faça logout e login novamente

### Erro: "Permission denied"

- Verifique se o usuário tem o perfil correto
- Verifique as permissões no Django Admin

## 📊 Verificar Instalação

Execute este comando para verificar se tudo está OK:

```powershell
python manage.py check --deploy
```

## 🔐 Configuração de Produção

### 1. Criar arquivo .env

```powershell
copy .env.example .env
```

### 2. Editar .env com suas configurações

```
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seu-dominio.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sgp_db
DB_USER=sgp_user
DB_PASSWORD=senha-segura
DB_HOST=localhost
DB_PORT=5432
```

### 3. Configurar PostgreSQL

```sql
CREATE DATABASE sgp_db;
CREATE USER sgp_user WITH PASSWORD 'senha-segura';
GRANT ALL PRIVILEGES ON DATABASE sgp_db TO sgp_user;
```

### 4. Executar Migrações

```powershell
python manage.py migrate
```

### 5. Coletar Arquivos Estáticos

```powershell
python manage.py collectstatic
```

### 6. Iniciar com Gunicorn

```powershell
gunicorn --bind 0.0.0.0:8000 --workers 3 sgp.wsgi:application
```

## 🐳 Usando Docker

### Iniciar com Docker Compose

```powershell
docker-compose up -d
```

### Ver Logs

```powershell
docker-compose logs -f web
```

### Executar Migrações no Container

```powershell
docker-compose exec web python manage.py migrate
```

### Criar Superusuário no Container

```powershell
docker-compose exec web python manage.py createsuperuser
```

### Parar Containers

```powershell
docker-compose down
```

## 📝 Próximos Passos

1. ✅ Executar os comandos acima
2. ✅ Acessar o admin em http://localhost:8000/admin
3. ✅ Criar alguns projetos de teste
4. ✅ Testar o workflow completo
5. ✅ Implementar serializers e views da API REST
6. ✅ Implementar testes automatizados
7. ✅ Configurar ambiente de produção

## 🎯 Checklist de Inicialização

- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Migrações criadas
- [ ] Migrações aplicadas
- [ ] Diretórios criados
- [ ] Usuários de exemplo criados
- [ ] Servidor iniciado
- [ ] Admin acessível
- [ ] Login funcionando

## 📞 Suporte

Se encontrar problemas, verifique:
1. README.md - Documentação completa
2. QUICK_START.md - Guia rápido
3. ARCHITECTURE.md - Arquitetura do sistema
4. SISTEMA_IMPLEMENTADO.md - Detalhes da implementação

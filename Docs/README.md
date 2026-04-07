# Sistema de Gestão de Portfólio de Projetos (SGP)

Sistema Django para gestão da carteira de projetos estratégicos do ITEC, implementado seguindo as melhores práticas de Django 6.0 e DevSecOps.

## 🚀 Características

- **Gestão Completa de Projetos**: Submissão, avaliação, priorização e acompanhamento
- **Workflow Automatizado**: Fluxo de aprovação com 9 etapas (Submissão → Aceite)
- **Sistema de Pontuação**: Avaliação em 3 etapas (A: 0-25, B: 0-25, C: 0-60 pontos)
- **RBAC (Role-Based Access Control)**: 6 perfis de usuário com permissões específicas
- **Auditoria Completa**: Logs imutáveis de todas as ações do sistema
- **API REST**: Endpoints completos para integração
- **Segurança**: Implementação de boas práticas de segurança (HTTPS, CORS, CSP, etc.)

## 📋 Requisitos

- Python 3.12+
- PostgreSQL 16+
- Redis 7+
- Docker & Docker Compose (opcional)

## 🔧 Instalação

### Usando Docker (Recomendado)

```bash
# Clone o repositório
git clone <repository-url>
cd sgp

# Copie o arquivo de ambiente
cp .env.example .env

# Edite o .env com suas configurações
# nano .env

# Inicie os containers
docker-compose up -d

# Execute as migrações
docker-compose exec web python manage.py migrate

# Crie um superusuário
docker-compose exec web python manage.py createsuperuser

# Acesse o sistema
# http://localhost:8000/admin
```

### Instalação Manual

```bash
# Clone o repositório
git clone <repository-url>
cd sgp

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Copie o arquivo de ambiente
cp .env.example .env

# Configure o banco de dados PostgreSQL
# Edite o .env com suas credenciais

# Execute as migrações
python manage.py migrate

# Crie um superusuário
python manage.py createsuperuser

# Colete arquivos estáticos
python manage.py collectstatic

# Inicie o servidor
python manage.py runserver
```

## 🏗️ Estrutura do Projeto

```
sgp/
├── usuarios/           # Gestão de usuários e perfis
├── projetos/          # Modelos de projetos, recursos, indicadores
├── avaliacoes/        # Avaliações, viabilidade e priorização
├── carteira/          # Carteiras, validação, deliberação
├── auditoria/         # Logs de auditoria, notificações
├── sgp/               # Configurações do projeto
├── Docs/              # Documentação
├── logs/              # Arquivos de log
├── media/             # Arquivos de upload
└── staticfiles/       # Arquivos estáticos
```

## 👥 Perfis de Usuário

1. **Demandante**: Submete projetos
2. **SUPRN**: Avalia projetos (Etapas A e B)
3. **Gerente de Projeto**: Gerencia execução de projetos
4. **Gerente de Portfólio**: Prioriza e consolida carteira
5. **Coordenador**: Valida carteira
6. **Presidência**: Delibera sobre aprovação final

## 🔄 Fluxo de Trabalho

```
1. RASCUNHO → 2. SUBMETIDO → 3. EM_AVALIACAO → 4. EM_VIABILIDADE → 
5. EM_PRIORIZACAO → 6. EM_CONSOLIDACAO → 7. EM_VALIDACAO → 
8. EM_DELIBERACAO → 9. AGUARDANDO_COMUNICACAO → 10. COMUNICADO → 11. ACEITO
```

## 📊 Sistema de Pontuação

- **Etapa A**: Alinhamento Estratégico (0-25 pontos)
- **Etapa B**: Impacto e Benefícios (0-25 pontos)
- **Etapa C**: Critérios Ponderados (0-60 pontos)
- **Total Máximo**: 110 pontos

## 🔐 Segurança

### Implementações de Segurança

- ✅ Autenticação via Token e Session
- ✅ HTTPS obrigatório em produção
- ✅ CORS configurado
- ✅ XSS Protection
- ✅ CSRF Protection
- ✅ Clickjacking Protection
- ✅ Content Type Nosniff
- ✅ HSTS (HTTP Strict Transport Security)
- ✅ Validação de arquivos upload
- ✅ Logs imutáveis de auditoria
- ✅ Rate limiting (via middleware)

### Variáveis de Ambiente Sensíveis

Nunca commite o arquivo `.env`. Use `.env.example` como template.

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html

# Testes específicos
pytest projetos/tests/
```

## 📈 Monitoramento

### Logs

Os logs são armazenados em:
- `logs/sgp.log` - Log geral da aplicação
- Logs de auditoria no banco de dados (tabela `audit_logs`)

### Health Check

```bash
curl http://localhost:8000/health/
```

## 🔍 Análise de Segurança

```bash
# SAST - Bandit
bandit -r . -f json -o bandit-report.json

# Verificação de dependências
safety check

# Linting
flake8 .
black --check .
isort --check-only .

# Type checking
mypy .
```

## 🚀 Deploy

### Produção

1. Configure as variáveis de ambiente em `.env`
2. Configure `DEBUG=False`
3. Configure `SECRET_KEY` seguro
4. Configure banco de dados PostgreSQL
5. Configure servidor de email
6. Configure Sentry para monitoramento de erros
7. Use gunicorn + nginx
8. Configure SSL/TLS

```bash
# Exemplo com gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 3 sgp.wsgi:application
```

## 📚 API REST

### Autenticação

```bash
# Obter token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'

# Usar token
curl -X GET http://localhost:8000/api/projetos/ \
  -H "Authorization: Token <seu-token>"
```

### Endpoints Principais

- `GET /api/projetos/` - Lista projetos
- `POST /api/projetos/` - Cria projeto
- `GET /api/projetos/{id}/` - Detalhes do projeto
- `PUT /api/projetos/{id}/` - Atualiza projeto
- `POST /api/projetos/{id}/submeter/` - Submete projeto
- `GET /api/avaliacoes/` - Lista avaliações
- `GET /api/carteiras/` - Lista carteiras
- `GET /api/audit-logs/` - Logs de auditoria

## 🛠️ Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Shell interativo
python manage.py shell

# Verificar problemas
python manage.py check

# Executar testes
python manage.py test
```

## 📝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto é proprietário do ITEC.

## 👨‍💻 Suporte

Para suporte, entre em contato com a equipe de desenvolvimento do ITEC.

## 🔄 Changelog

### v1.0.0 (2026-04-06)
- ✅ Implementação inicial do sistema
- ✅ Modelos completos de projetos, avaliações e carteiras
- ✅ Sistema de autenticação e RBAC
- ✅ API REST completa
- ✅ Sistema de auditoria com logs imutáveis
- ✅ Configurações de segurança DevSecOps
- ✅ Docker e CI/CD configurados

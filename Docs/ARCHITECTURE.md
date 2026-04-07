# Arquitetura do Sistema SGP

## 📐 Visão Geral

O Sistema de Gestão de Portfólio de Projetos (SGP) é construído usando Django 6.0 seguindo a arquitetura MVT (Model-View-Template) com API REST.

## 🏗️ Camadas da Aplicação

```
┌─────────────────────────────────────────┐
│         Frontend / API Clients          │
├─────────────────────────────────────────┤
│         API REST (DRF)                  │
├─────────────────────────────────────────┤
│         Views & Serializers             │
├─────────────────────────────────────────┤
│         Business Logic                  │
├─────────────────────────────────────────┤
│         Models (ORM)                    │
├─────────────────────────────────────────┤
│         Database (PostgreSQL)           │
└─────────────────────────────────────────┘
```

## 📦 Estrutura de Apps

### 1. **usuarios** - Gestão de Usuários
- Modelo customizado de usuário
- Sistema RBAC com 6 perfis
- Autenticação e autorização

**Modelos:**
- `Usuario` - Usuário customizado com perfil

### 2. **projetos** - Gestão de Projetos
- CRUD completo de projetos
- Gestão de recursos e indicadores
- Upload de documentos

**Modelos:**
- `Projeto` - Projeto estratégico
- `Recurso` - Recursos do projeto
- `Indicador` - Indicadores de desempenho
- `Documento` - Documentos anexados

### 3. **avaliacoes** - Avaliações e Priorizações
- Avaliação em 3 etapas (A, B, C)
- Análise de viabilidade
- Sistema de pontuação

**Modelos:**
- `Avaliacao` - Avaliação do projeto
- `CriterioAvaliacaoA` - Critérios etapa A
- `CriterioAvaliacaoB` - Critérios etapa B
- `Viabilidade` - Análise de viabilidade
- `Priorizacao` - Priorização do projeto
- `CriterioPriorizacao` - Critérios de priorização

### 4. **carteira** - Gestão de Carteiras
- Consolidação de projetos
- Validação e deliberação
- Comunicação e aceite

**Modelos:**
- `Carteira` - Carteira de projetos
- `ProjetoCarteira` - Relação projeto-carteira
- `Validacao` - Validação da carteira
- `Deliberacao` - Deliberação final
- `Comunicacao` - Comunicações
- `Aceite` - Aceite do projeto

### 5. **auditoria** - Auditoria e Logs
- Logs imutáveis
- Histórico de mudanças
- Notificações
- Anexos genéricos

**Modelos:**
- `AuditLog` - Log de auditoria (imutável)
- `HistoricoStatus` - Histórico de status
- `Notificacao` - Notificações
- `Anexo` - Anexos genéricos

## 🔄 Fluxo de Dados

### Workflow de Projeto

```
┌──────────────┐
│  DEMANDANTE  │
│   Cria       │
│   Projeto    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   RASCUNHO   │
└──────┬───────┘
       │ Submete
       ▼
┌──────────────┐
│  SUBMETIDO   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    SUPRN     │
│   Avalia     │
│  (Etapas A+B)│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ EM_AVALIACAO │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Análise de   │
│ Viabilidade  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   GERENTE    │
│  PORTFOLIO   │
│  Prioriza    │
│  (Etapa C)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Consolidação │
│  da Carteira │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ COORDENADOR  │
│   Valida     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ PRESIDÊNCIA  │
│  Delibera    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Comunicação  │
│   e Aceite   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    ACEITO    │
└──────────────┘
```

## 🔐 Segurança

### Camadas de Segurança

1. **Autenticação**
   - Token Authentication (DRF)
   - Session Authentication
   - Password hashing (PBKDF2)

2. **Autorização**
   - RBAC baseado em perfis
   - Permissões por modelo
   - Verificação em views e serializers

3. **Proteção de Dados**
   - HTTPS obrigatório (produção)
   - CSRF Protection
   - XSS Protection
   - SQL Injection (ORM)

4. **Auditoria**
   - Logs imutáveis
   - Rastreamento de IP
   - User Agent tracking
   - Histórico completo

### Matriz de Permissões

| Perfil              | Criar Projeto | Avaliar | Priorizar | Validar | Deliberar |
|---------------------|---------------|---------|-----------|---------|-----------|
| Demandante          | ✅            | ❌      | ❌        | ❌      | ❌        |
| SUPRN               | ❌            | ✅      | ❌        | ❌      | ❌        |
| Gerente Projeto     | ❌            | ❌      | ❌        | ❌      | ❌        |
| Gerente Portfólio   | ❌            | ❌      | ✅        | ❌      | ❌        |
| Coordenador         | ❌            | ❌      | ❌        | ✅      | ❌        |
| Presidência         | ❌            | ❌      | ❌        | ❌      | ✅        |

## 💾 Modelo de Dados

### Relacionamentos Principais

```
Usuario (1) ──────── (N) Projeto
                         │
                         ├── (N) Recurso
                         ├── (N) Indicador
                         ├── (N) Documento
                         ├── (N) Avaliacao
                         ├── (N) Viabilidade
                         ├── (N) Priorizacao
                         └── (N) HistoricoStatus

Carteira (1) ──────── (N) ProjetoCarteira ──────── (1) Projeto
    │
    ├── (N) Validacao
    ├── (N) Deliberacao
    └── (N) Comunicacao

AuditLog (logs de todas as operações)
```

## 🔧 Tecnologias Utilizadas

### Backend
- **Django 6.0** - Framework web
- **Django REST Framework** - API REST
- **PostgreSQL** - Banco de dados
- **Redis** - Cache e Celery broker
- **Celery** - Tarefas assíncronas

### DevOps
- **Docker** - Containerização
- **Docker Compose** - Orquestração
- **GitHub Actions** - CI/CD
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy (produção)

### Segurança
- **Bandit** - SAST
- **Safety** - Verificação de dependências
- **Trivy** - Scanner de vulnerabilidades
- **Sentry** - Monitoramento de erros

### Qualidade de Código
- **Pytest** - Testes
- **Coverage** - Cobertura de testes
- **Black** - Formatação
- **Flake8** - Linting
- **isort** - Organização de imports
- **mypy** - Type checking

## 📊 Performance

### Otimizações Implementadas

1. **Database**
   - Índices em campos frequentemente consultados
   - Select related / Prefetch related
   - Paginação de resultados

2. **Caching**
   - Redis para cache de sessões
   - Cache de queries frequentes

3. **Files**
   - Upload assíncrono de arquivos
   - Validação de tipos e tamanhos

## 🚀 Escalabilidade

### Horizontal Scaling
- Stateless application
- Session storage em Redis
- Media files em S3 (produção)

### Vertical Scaling
- Connection pooling
- Query optimization
- Async tasks com Celery

## 📈 Monitoramento

### Métricas Coletadas
- Tempo de resposta das APIs
- Taxa de erros
- Uso de recursos
- Logs de auditoria
- Eventos de segurança

### Ferramentas
- Sentry - Error tracking
- Logs estruturados
- Health checks
- Database monitoring

## 🔄 CI/CD Pipeline

```
┌─────────────┐
│   Commit    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Security    │
│ Scan        │
│ (Bandit)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Lint      │
│ (Flake8)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Tests     │
│  (Pytest)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Build     │
│  (Docker)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Deploy    │
│ (Production)│
└─────────────┘
```

## 📝 Convenções de Código

### Nomenclatura
- **Models**: PascalCase (ex: `Projeto`, `Usuario`)
- **Functions**: snake_case (ex: `criar_projeto`, `validar_carteira`)
- **Constants**: UPPER_CASE (ex: `STATUS_CHOICES`)
- **Variables**: snake_case (ex: `projeto_id`, `usuario_atual`)

### Estrutura de Arquivos
```
app/
├── __init__.py
├── admin.py          # Configuração do admin
├── apps.py           # Configuração do app
├── models.py         # Modelos de dados
├── serializers.py    # Serializers DRF
├── views.py          # Views/ViewSets
├── urls.py           # URLs do app
├── permissions.py    # Permissões customizadas
├── filters.py        # Filtros customizados
├── signals.py        # Signals Django
└── tests/            # Testes
    ├── test_models.py
    ├── test_views.py
    └── test_serializers.py
```

## 🎯 Próximas Melhorias

- [ ] Implementar cache Redis
- [ ] Adicionar testes automatizados
- [ ] Criar dashboard de métricas
- [ ] Implementar notificações por email
- [ ] Adicionar exportação de relatórios
- [ ] Implementar versionamento de documentos
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Criar aplicativo mobile

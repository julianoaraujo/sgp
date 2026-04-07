# Guia de Ferramentas de Qualidade de Código

## 📦 Instalação

Instale as ferramentas de desenvolvimento (opcional, apenas se quiser usar):

```powershell
pip install -r requirements-dev.txt
```

---

## 🎨 Black - Formatador de Código

**O que faz:** Formata automaticamente seu código Python seguindo um estilo consistente.

### Como usar:

```powershell
# Formatar todos os arquivos
black .

# Formatar arquivo específico
black usuarios/models.py

# Ver o que seria alterado (sem modificar)
black --check .

# Ver diferenças
black --diff .
```

### Exemplo:
**Antes:**
```python
def minha_funcao(x,y,z):
    return x+y+z
```

**Depois:**
```python
def minha_funcao(x, y, z):
    return x + y + z
```

---

## 📋 isort - Organizador de Imports

**O que faz:** Organiza e agrupa seus imports automaticamente.

### Como usar:

```powershell
# Organizar imports de todos os arquivos
isort .

# Organizar arquivo específico
isort usuarios/models.py

# Ver o que seria alterado
isort --check .

# Ver diferenças
isort --diff .
```

### Exemplo:
**Antes:**
```python
from django.db import models
import os
from usuarios.models import Usuario
import sys
from django.contrib.auth import authenticate
```

**Depois:**
```python
import os
import sys

from django.contrib.auth import authenticate
from django.db import models

from usuarios.models import Usuario
```

---

## 🔍 Flake8 - Verificador de Estilo

**O que faz:** Verifica se seu código segue as boas práticas Python (PEP 8).

### Como usar:

```powershell
# Verificar todo o projeto
flake8

# Verificar arquivo específico
flake8 usuarios/models.py

# Verificar com mais detalhes
flake8 --show-source --statistics
```

### O que detecta:
- ❌ Linhas muito longas
- ❌ Imports não utilizados
- ❌ Variáveis não utilizadas
- ❌ Espaçamento incorreto
- ❌ Indentação errada

---

## 🔒 Bandit - Análise de Segurança

**O que faz:** Detecta vulnerabilidades de segurança no código.

### Como usar:

```powershell
# Analisar todo o projeto
bandit -r .

# Analisar com relatório detalhado
bandit -r . -f json -o relatorio_seguranca.json

# Analisar apenas severidade alta
bandit -r . -ll
```

### O que detecta:
- 🔒 Senhas hardcoded
- 🔒 SQL injection
- 🔒 Uso de `eval()` ou `exec()`
- 🔒 Imports inseguros
- 🔒 Uso de funções criptográficas fracas

---

## 🛡️ Safety - Verificador de Dependências

**O que faz:** Verifica se suas dependências têm vulnerabilidades conhecidas.

### Como usar:

```powershell
# Verificar vulnerabilidades
safety check

# Verificar com mais detalhes
safety check --full-report

# Gerar relatório JSON
safety check --json
```

---

## 🔤 mypy - Verificador de Tipos

**O que faz:** Verifica tipos estáticos para prevenir erros.

### Como usar:

```powershell
# Verificar todo o projeto
mypy .

# Verificar arquivo específico
mypy usuarios/models.py

# Verificar com mais rigor
mypy --strict .
```

### Exemplo:
```python
# mypy detecta erro de tipo
def somar(a: int, b: int) -> int:
    return a + b

resultado = somar(5, "10")  # ❌ Erro: esperava int, recebeu str
```

---

## 🧪 Pytest - Testes Automatizados

**O que faz:** Executa testes automatizados do seu código.

### Como usar:

```powershell
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=.

# Executar testes específicos
pytest usuarios/tests.py

# Executar com mais detalhes
pytest -v

# Gerar relatório HTML de cobertura
pytest --cov=. --cov-report=html
```

---

## 🚀 Workflow Recomendado

### Antes de fazer commit:

```powershell
# 1. Formatar código
black .
isort .

# 2. Verificar estilo
flake8

# 3. Verificar segurança
bandit -r .

# 4. Executar testes
pytest

# 5. Verificar cobertura
pytest --cov=.
```

### Ou use um único comando (crie um script):

Crie `check.ps1`:
```powershell
Write-Host "🎨 Formatando código..." -ForegroundColor Cyan
black .
isort .

Write-Host "`n🔍 Verificando estilo..." -ForegroundColor Cyan
flake8

Write-Host "`n🔒 Verificando segurança..." -ForegroundColor Cyan
bandit -r . -ll

Write-Host "`n🧪 Executando testes..." -ForegroundColor Cyan
pytest --cov=.

Write-Host "`n✅ Verificação completa!" -ForegroundColor Green
```

Execute:
```powershell
.\check.ps1
```

---

## 📝 Integração com Git (Pre-commit)

Para executar automaticamente antes de cada commit, instale:

```powershell
pip install pre-commit
```

Crie `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks:
      - id: black
  
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
  
  - repo: https://github.com/PyCQA/flake8
    rev: 7.1.1
    hooks:
      - id: flake8
```

Ative:
```powershell
pre-commit install
```

Agora as verificações rodam automaticamente antes de cada commit! 🎉

---

## 💡 Dicas

1. **Comece aos poucos**: Use apenas Black e isort no início
2. **Configure seu editor**: VSCode e PyCharm têm plugins para essas ferramentas
3. **Ignore arquivos**: migrations, venv, etc. (já configurado nos arquivos)
4. **CI/CD**: Adicione essas verificações no GitHub Actions (já configurado)

---

## ⚙️ Configurações

Todas as configurações estão em:
- `pyproject.toml` - Black, isort, mypy
- `.flake8` - Flake8
- `.bandit` - Bandit

Você pode ajustar conforme necessário!

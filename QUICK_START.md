# Guia de Início Rápido - SGP

## 🚀 Início Rápido (5 minutos)

### Passo 1: Preparar o Ambiente

```bash
# Ative o ambiente virtual
vProjetime26\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### Passo 2: Configurar Banco de Dados

```bash
# Criar as tabelas no banco de dados
python manage.py makemigrations
python manage.py migrate
```

### Passo 3: Inicializar o Sistema

```bash
# Criar diretórios e usuários de exemplo
python init_system.py

# OU criar apenas um superusuário
python manage.py createsuperuser
```

### Passo 4: Iniciar o Servidor

```bash
python manage.py runserver
```

### Passo 5: Acessar o Sistema

Abra seu navegador em: **http://localhost:8000/admin**

**Usuários de exemplo criados:**
- `demandante1` / `senha123` - Perfil Demandante
- `suprn1` / `senha123` - Perfil SUPRN
- `gerente_portfolio1` / `senha123` - Perfil Gerente de Portfólio
- `coordenador1` / `senha123` - Perfil Coordenador
- `presidencia1` / `senha123` - Perfil Presidência

## 📋 Próximos Passos

### 1. Criar um Projeto

1. Faça login como `demandante1`
2. Acesse **Projetos** → **Adicionar Projeto**
3. Preencha os dados obrigatórios
4. Salve como rascunho

### 2. Submeter o Projeto

1. Abra o projeto criado
2. Clique em "Submeter Projeto"
3. O status mudará para "Submetido"

### 3. Avaliar o Projeto

1. Faça logout e login como `suprn1`
2. Acesse **Avaliações** → **Adicionar Avaliação**
3. Selecione o projeto submetido
4. Preencha as pontuações das Etapas A e B
5. Salve a avaliação

### 4. Análise de Viabilidade

1. Acesse **Viabilidades** → **Adicionar Análise**
2. Selecione o projeto
3. Preencha as análises técnica, financeira, operacional e jurídica
4. Defina o resultado (Viável/Inviável)

### 5. Priorizar o Projeto

1. Faça login como `gerente_portfolio1`
2. Acesse **Priorizações** → **Adicionar Priorização**
3. Defina complexidade, urgência e impacto estratégico
4. Preencha a pontuação da Etapa C

### 6. Criar Carteira

1. Acesse **Carteiras** → **Adicionar Carteira**
2. Defina ano e período
3. Adicione projetos priorizados à carteira
4. Defina o ranking dos projetos

### 7. Validar Carteira

1. Faça login como `coordenador1`
2. Acesse a carteira criada
3. Crie uma validação
4. Aprove ou solicite ajustes

### 8. Deliberar

1. Faça login como `presidencia1`
2. Acesse a carteira validada
3. Crie uma deliberação
4. Aprove a carteira

## 🔧 Comandos Úteis

```bash
# Ver logs em tempo real
tail -f logs/sgp.log

# Criar backup do banco
python manage.py dumpdata > backup.json

# Restaurar backup
python manage.py loaddata backup.json

# Limpar sessões expiradas
python manage.py clearsessions

# Verificar problemas
python manage.py check --deploy
```

## 🐛 Solução de Problemas

### Erro: "No module named 'rest_framework'"
```bash
pip install -r requirements.txt
```

### Erro: "Table doesn't exist"
```bash
python manage.py migrate
```

### Erro: "CSRF verification failed"
- Limpe os cookies do navegador
- Verifique se está usando HTTPS em produção

### Erro: "Permission denied"
- Verifique se o usuário tem o perfil correto
- Verifique as permissões no admin

## 📚 Documentação Adicional

- **README.md** - Documentação completa
- **Docs/levantamentoRequisitos.md** - Requisitos do sistema
- **API Documentation** - http://localhost:8000/api/ (quando implementada)

## 🔐 Segurança

⚠️ **IMPORTANTE**: 
- Altere a `SECRET_KEY` em produção
- Configure `DEBUG=False` em produção
- Use HTTPS em produção
- Configure backup automático do banco de dados
- Monitore os logs de auditoria regularmente

## 📞 Suporte

Para dúvidas ou problemas, consulte a documentação ou entre em contato com a equipe de desenvolvimento.

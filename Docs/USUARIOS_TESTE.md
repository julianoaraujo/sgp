# Usuários de Teste - SGP

## Como Criar os Usuários

Execute o seguinte comando para criar todos os usuários de teste:

```bash
python manage.py shell < create_test_users.py
```

## Credenciais de Acesso

| Perfil | Usuário | Senha | Função |
|--------|---------|-------|--------|
| **Superadmin** | `jafar` | `Z{H\swl,S_Vt2pg~l@7G` | Acesso total ao sistema |
| **SUPRN** | `suprn` | `suprn123` | Avaliar projetos (Etapas A e B) |
| **Demandante** | `demandante` | `demandante123` | Criar e submeter projetos |
| **Gerente de Projeto** | `gerente_projeto` | `gerente123` | Gerenciar projetos |
| **Gerente de Portfólio** | `gerente_portfolio` | `portfolio123` | Priorizar projetos (Etapa C) |
| **Coordenador** | `coordenador` | `coordenador123` | Validar carteiras |
| **Presidência** | `presidencia` | `presidencia123` | Deliberar e aprovar |

## Fluxo de Teste Completo

### 1. Criar Projeto (Demandante ou Superadmin)
- Login: `demandante` / `demandante123` ou `jafar`
- Criar novo projeto
- Preencher informações
- **Submeter** o projeto

### 2. Avaliar Projeto (SUPRN)
- Login: `suprn` / `suprn123`
- Acessar menu "Avaliações"
- Ver projetos submetidos
- Clicar em "Avaliar"
- Preencher Etapa A (0-25 pontos)
- Preencher Etapa B (0-25 pontos)
- Adicionar parecer técnico
- Salvar avaliação

### 3. Análise de Viabilidade (SUPRN ou Gerente Portfólio)
- Login: `suprn` ou `gerente_portfolio`
- Abrir projeto avaliado
- Clicar em "Viabilidade"
- Analisar viabilidade técnica, financeira, operacional e jurídica
- Definir resultado (Viável/Viável com Restrições/Inviável)
- Salvar análise

### 4. Priorização (Gerente Portfólio, Coordenador ou Presidência)
- Login: `gerente_portfolio` / `portfolio123`
- Abrir projeto com viabilidade aprovada
- Clicar em "Priorizar"
- Preencher Etapa C (0-60 pontos)
- Definir complexidade, urgência e impacto
- Salvar priorização
- **Pontuação total** = A + B + C (máximo 110 pontos)

### 5. Consolidar Carteira (Gerente Portfólio)
- Login: `gerente_portfolio`
- Acessar "Carteiras"
- Criar nova carteira
- Adicionar projetos priorizados
- Ordenar por pontuação

### 6. Validar Carteira (Coordenador)
- Login: `coordenador` / `coordenador123`
- Revisar carteira consolidada
- Validar ou solicitar ajustes

### 7. Deliberar (Presidência)
- Login: `presidencia` / `presidencia123`
- Revisar carteira validada
- Aprovar ou rejeitar

## Permissões por Perfil

### DEMANDANTE
- ✅ Criar projetos
- ✅ Submeter projetos
- ✅ Visualizar próprios projetos

### SUPRN
- ✅ Avaliar projetos (Etapas A e B)
- ✅ Análise de viabilidade
- ✅ Visualizar todas as avaliações

### GERENTE_PROJETO
- ✅ Gerenciar projetos atribuídos
- ✅ Atualizar status de execução

### GERENTE_PORTFOLIO
- ✅ Priorizar projetos (Etapa C)
- ✅ Consolidar carteiras
- ✅ Análise de viabilidade

### COORDENADOR
- ✅ Validar carteiras
- ✅ Priorizar projetos
- ✅ Aprovar projetos

### PRESIDÊNCIA
- ✅ Deliberar sobre carteiras
- ✅ Aprovação final
- ✅ Acesso total (is_staff)

## Notas Importantes

- Todos os usuários de teste têm senhas simples para facilitar os testes
- Em produção, use senhas fortes e altere-as regularmente
- O superadmin `jafar` tem acesso total ao Django Admin
- Recomenda-se criar novos usuários com senhas seguras para produção

# Change: search-subjects-overdue

## Why
O usuário precisa localizar disciplinas de forma eficiente filtrando por:
1. **Nome da disciplina** (busca textual)
2. **Tarefas atrasadas** (integração com tabela `academic_tasks`)

Atualmente, não há endpoint de busca avançado. O usuário deve percorrer manualmente todas as disciplinas, dificultando a identificação de disciplinas com atividades pendentes.

## What Changes
Criar endpoint REST `GET /subjects/search` que:
- Aceita parâmetros de filtro: `?name=<texto>` e `?has_overdue=true`
- Retorna disciplinas filtradas com informações agregadas sobre tarefas atrasadas
- Integra lógica XanoScript com (opcional) pós-processamento em Python

## Impact
- **Melhoria UX:** Usuários localizam rapidamente disciplinas com tarefas pendentes
- **Escalabilidade:** Reduz carga de cliente ao filtrar no backend
- **Flexibilidade:** Suporta múltiplos critérios de busca (nome + status de tarefas)

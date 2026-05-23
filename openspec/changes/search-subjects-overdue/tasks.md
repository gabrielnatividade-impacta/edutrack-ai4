# Tasks: search-subjects-overdue

## Implementation Checklist

- [x] Criar função XanoScript `calculate_overdue_count` em `functions/search_helpers/`
  - Input: `subject_id` (uuid)
  - Output: `{overdue_count: int, overdue_tasks: array}`
  - Query: `academic_tasks WHERE subject_id = ? AND due_date < now AND status != "completed"`
  - ✅ Implementado em: `functions/search_helpers/calculate_overdue_count.xs`
  
- [x] Criar API endpoint `GET /subjects/search` em `apis/search/`
  - Autenticação: `auth = "user"`
  - Query params: `name` (text), `has_overdue` (boolean)
  - Filtro by-name: `WHERE name LIKE %search%` (case-insensitive)
  - Enriquecer com overdue_count via função helper
  - Response: Array de subjects com agregações
  - ✅ Implementado em: `apis/search/3600300_subjects_search_GET.xs`

- [x] Integrar no frontend Streamlit (`pages/disciplines.py`)
  - Adicionar campo de busca textual
  - Adicionar checkbox "Mostrar apenas com tarefas atrasadas"
  - Chamar `GET /subjects/search` com parâmetros
  - Exibir resultados em tabela
  - ✅ Implementado com abas, expandores e tratamento de erros

- [ ] Criar testes unitários para `calculate_overdue_count`
  - Caso 1: Nenhuma tarefa atrasada
  - Caso 2: Uma tarefa atrasada
  - Caso 3: Múltiplas tarefas atrasadas e completas
  - Status: Pendente (próxima fase)

- [ ] Documentar no README: Como usar o endpoint de busca
  - Status: Pendente (próxima fase)

## Notes
- Integração Python é opcional: o Streamlit pode chamar o endpoint Xano via `requests.get()`
- Se pós-processamento adicional for necessário, adicionar lógica em `functions/search_helpers.py`

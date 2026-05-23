# Design: search-subjects-overdue

## Architecture Overview

### Components
1. **Function Helper (XanoScript)**: `calculate_overdue_count`
   - Calcula o número de tarefas atrasadas para uma disciplina
   - Input: `subject_id`
   - Output: `{count: int, tasks: array}`

2. **API Endpoint (XanoScript)**: `GET /subjects/search`
   - Localização: `apis/search/3600xxx_subjects_search_GET.xs`
   - Recebe query params: `?name=<search_text>` e `?has_overdue=<true|false>`
   - Filtra tabela `subjects` por `name` (LIKE query)
   - Para cada disciplina, calcula tarefas atrasadas usando a função helper
   - Retorna lista de disciplinas com agregações

3. **Filter Logic (Python - Opcional)**
   - Se a lógica XanoScript ficar complexa, pode-se adicionar pós-processamento em Python no Streamlit
   - Exemplo: enriquecer resposta com cálculos adicionais

## Data Flow
```
User Query (?name=xyz&has_overdue=true)
  ↓
API GET /subjects/search
  ↓
XanoScript: db.query subjects WHERE name LIKE ?
  ↓
For each subject: Call calculate_overdue_count function
  ↓
Filter by has_overdue flag
  ↓
Response: [{id, name, code, status, overdue_count, tasks[]}]
```

## Implementation Strategy
1. Criar função helper `calculate_overdue_count` em `functions/`
2. Criar endpoint `GET /subjects/search` em `apis/search/`
3. Integrar com frontend Streamlit (chamada via `requests`)
4. Adicionar testes unitários na função helper

## Error Handling
- `400 Bad Request`: Parâmetros inválidos
- `401 Unauthorized`: Usuário não autenticado
- `200 OK`: Retorna array vazio se nenhuma disciplina atender critérios

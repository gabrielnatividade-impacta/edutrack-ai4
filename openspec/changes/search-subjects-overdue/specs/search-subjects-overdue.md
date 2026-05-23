# search-subjects-overdue Specification

## Purpose
Define o endpoint de busca avançada de disciplinas com filtros por nome e status de tarefas atrasadas.

## ADDED Requirements

### Requirement: Search subjects by name
O sistema DEVE permitir filtrar disciplinas pelo nome usando busca case-insensitive.

#### Scenario: User searches for subject by name
- **WHEN** usuário executa `GET /subjects/search?name=math`
- **THEN** endpoint retorna todas as disciplinas do usuário que contenham "math" no nome (case-insensitive)

### Requirement: Identify subjects with overdue tasks
O sistema DEVE calcular e retornar o número de tarefas atrasadas por disciplina.

#### Scenario: Identify overdue tasks
- **WHEN** usuário executa `GET /subjects/search?has_overdue=true`
- **THEN** endpoint retorna somente disciplinas que possuem tarefas com `due_date < now` e `status != "completed"`

### Requirement: Combined filtering
O sistema DEVE suportar filtros combinados (nome + tarefas atrasadas).

#### Scenario: Search with multiple criteria
- **WHEN** usuário executa `GET /subjects/search?name=math&has_overdue=true`
- **THEN** endpoint retorna disciplinas que atendem AMBOS os critérios

### Requirement: Response with aggregated data
O endpoint DEVE retornar disciplinas com informações agregadas de tarefas.

#### Scenario: Response structure
- **WHEN** endpoint processa a busca
- **THEN** retorna `[{id, name, code, description, status, user_id, overdue_count, overdue_tasks: [{id, title, due_date, status}]}]`

### Requirement: Authentication and authorization
O endpoint DEVE validar que o usuário está autenticado e retornar somente suas disciplinas.

#### Scenario: User can only see their subjects
- **WHEN** usuário autenticado executa `/subjects/search`
- **THEN** retorna somente disciplinas onde `user_id == $auth.id`

## Backend Implementation Details

### Function: calculate_overdue_count
```
Input: subject_id (uuid)
Process:
  1. Query academic_tasks WHERE subject_id = ? AND due_date < now AND status != "completed"
  2. Return {count: int, tasks: array}
```

### Endpoint: GET /subjects/search
```
Path: GET /subjects/search
Auth: Required (user)
Query Params:
  - name (optional): Text search
  - has_overdue (optional): Boolean filter

Logic:
  1. Query subjects WHERE user_id = $auth.id
  2. If name provided: Filter WHERE name LIKE %name%
  3. For each subject: Calculate overdue_count
  4. If has_overdue=true: Filter subjects WHERE overdue_count > 0
  5. Return aggregated results
```

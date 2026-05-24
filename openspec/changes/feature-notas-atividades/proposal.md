## Why

Professores precisam de uma forma eficiente para lançar notas dos alunos nas atividades específicas. Atualmente, o sistema não possui um mecanismo para registrar e gerenciar grades das atividades por aluno, limitando a capacidade de acompanhamento de desempenho.

## What Changes

- Nova funcionalidade de lançamento de notas: professores podem registrar notas numéricas para cada aluno em atividades específicas
- API POST para criar registros de grades
- Estrutura de dados para armazenar notas com rastreamento de professor responsável e data

## Capabilities

### New Capabilities
- `activity-grades`: Permite que professores lancem notas para alunos em atividades acadêmicas específicas

### Modified Capabilities
<!-- Nenhuma capacidade existente é modificada em sua especificação -->

## Impact

- **Database**: Nova tabela `activity_grades` para armazenar notas
- **APIs**: Nova rota POST `/academic_tasks/{task_id}/grades` para lançamento de notas
- **Backend**: Nova lógica de validação de permissões (apenas professores podem lançar notas)
- **Schema**: Relacionamentos com tabelas `users` (aluno e professor), `subjects` (disciplina) e `academic_tasks` (atividades)

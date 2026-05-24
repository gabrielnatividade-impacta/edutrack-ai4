# task-management Specification

## Purpose
Definir a gestão completa de tarefas acadêmicas vinculadas a disciplinas e ao usuário autenticado.

## ADDED Requirements

### Requirement: User can create a task
O sistema SHALL permitir que o usuário cadastre uma tarefa vinculada a uma disciplina, informando título, descrição e prazo.

#### Scenario: Cadastro de tarefa
- **WHEN** o usuário informa disciplina, título, descrição e prazo
- **THEN** o sistema cria a tarefa associada à disciplina e ao usuário corretos

### Requirement: User can list tasks
O sistema SHALL listar todas as tarefas do usuário agrupadas por disciplina ou por prazo.

#### Scenario: Agrupamento de tarefas
- **WHEN** o usuário escolhe agrupamento por disciplina ou prazo
- **THEN** o sistema exibe as tarefas próprias no agrupamento selecionado

### Requirement: User can update a task
O sistema SHALL permitir que o usuário edite os dados de uma tarefa própria.

#### Scenario: Edição de tarefa
- **WHEN** o usuário altera título, descrição, prazo, status ou prioridade
- **THEN** o sistema salva a tarefa atualizada

### Requirement: User can delete a task
O sistema SHALL permitir que o usuário exclua uma tarefa própria.

#### Scenario: Exclusão de tarefa
- **WHEN** o usuário confirma a exclusão de uma tarefa própria
- **THEN** o sistema remove a tarefa

### Requirement: User can complete a task
O sistema SHALL permitir que o usuário marque uma tarefa como concluída.

#### Scenario: Marcar como concluída
- **WHEN** o usuário marca uma tarefa pendente ou em andamento como concluída
- **THEN** o sistema atualiza o status para completed

### Requirement: Filter tasks by status
O sistema SHALL permitir filtrar tarefas por status Pendente, Em andamento e Concluída.

#### Scenario: Filtro por status
- **WHEN** o usuário seleciona um status
- **THEN** o sistema exibe somente tarefas próprias com o status selecionado

### Requirement: Highlight overdue tasks
O sistema SHALL identificar e sinalizar visualmente tarefas com prazo vencido.

#### Scenario: Prazo vencido
- **WHEN** uma tarefa não concluída possui prazo anterior à data atual
- **THEN** o sistema exibe a tarefa com indicação visual de atraso

### Requirement: Task priority
O sistema SHALL permitir prioridade Baixa, Média ou Alta em tarefas.

#### Scenario: Tarefa com prioridade
- **WHEN** o usuário define prioridade da tarefa
- **THEN** o sistema armazena e exibe a prioridade selecionada

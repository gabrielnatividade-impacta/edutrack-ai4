# dashboard-reporting Specification

## Purpose
Definir dashboard, progresso, relatórios e exportação de dados do EduTrack AI.

## ADDED Requirements

### Requirement: Dashboard summary
O sistema SHALL exibir uma tela inicial após login com visão geral do sistema.

#### Scenario: Visão geral pós-login
- **WHEN** o usuário autenticado acessa a tela inicial
- **THEN** o sistema exibe total de disciplinas ativas, total de tarefas pendentes e total de tarefas em atraso

### Requirement: Dashboard upcoming tasks
O sistema SHALL exibir as próximas tarefas com prazo mais próximo.

#### Scenario: Próximas tarefas
- **WHEN** o usuário acessa o dashboard
- **THEN** o sistema lista tarefas próprias ordenadas pelos prazos mais próximos

### Requirement: General progress indicator
O sistema SHALL exibir indicador de progresso geral com percentual de tarefas concluídas.

#### Scenario: Cálculo de progresso geral
- **WHEN** o usuário possui tarefas cadastradas
- **THEN** o sistema calcula tarefas concluídas divididas pelo total de tarefas

### Requirement: Reports by period
O sistema SHALL criar uma tela de relatórios com histórico de tarefas por período.

#### Scenario: Histórico por período
- **WHEN** o usuário seleciona um período
- **THEN** o sistema exibe tarefas próprias dentro do período selecionado

### Requirement: Subject progress report
O sistema SHALL exibir progresso por disciplina com base nas tarefas concluídas.

#### Scenario: Progresso por disciplina
- **WHEN** o usuário abre relatórios ou detalhes da disciplina
- **THEN** o sistema exibe percentual de conclusão das tarefas da disciplina

### Requirement: Export academic data
O sistema SHALL permitir exportar disciplinas e tarefas em CSV ou PDF.

#### Scenario: Exportação de dados
- **WHEN** o usuário seleciona formato CSV ou PDF
- **THEN** o sistema gera arquivo contendo disciplinas e tarefas próprias

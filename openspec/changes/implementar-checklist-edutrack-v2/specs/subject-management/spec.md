# subject-management Specification

## Purpose
Atualizar a gestão de disciplinas para cobrir os campos e fluxos funcionais do checklist EduTrack AI.

## MODIFIED Requirements

### Requirement: User can create a subject
O sistema SHALL permitir que o usuário cadastre uma disciplina informando nome, professor e carga horária, vinculando a disciplina ao usuário autenticado.

#### Scenario: Cadastro de disciplina
- **WHEN** o usuário autenticado informa nome, professor e carga horária
- **THEN** o sistema cria a disciplina associada ao user_id do usuário logado

### Requirement: User can retrieve their subjects
O sistema SHALL listar todas as disciplinas do usuário autenticado.

#### Scenario: Listagem de disciplinas do usuário
- **WHEN** o usuário solicita suas disciplinas
- **THEN** o sistema retorna somente disciplinas vinculadas ao user_id autenticado

### Requirement: User can update their subject
O sistema SHALL permitir que o usuário edite os dados de uma disciplina própria.

#### Scenario: Edição de disciplina
- **WHEN** o usuário edita uma disciplina própria
- **THEN** o sistema salva os dados atualizados sem alterar o proprietário

### Requirement: User can delete their subject
O sistema SHALL permitir que o usuário exclua uma disciplina própria.

#### Scenario: Exclusão de disciplina
- **WHEN** o usuário confirma a exclusão de uma disciplina própria
- **THEN** o sistema remove a disciplina

## ADDED Requirements

### Requirement: Prevent duplicate subjects
O sistema SHALL impedir cadastro de disciplinas duplicadas com mesmo nome e professor para o mesmo usuário.

#### Scenario: Tentativa de duplicidade
- **WHEN** o usuário tenta cadastrar disciplina com mesmo nome e professor já existentes em sua conta
- **THEN** o sistema rejeita o cadastro

### Requirement: Search subjects by name
O sistema SHALL permitir buscar disciplinas por nome.

#### Scenario: Busca por nome
- **WHEN** o usuário informa um termo de busca
- **THEN** o sistema retorna disciplinas próprias cujo nome corresponde ao termo

### Requirement: Filter subjects with overdue tasks
O sistema SHALL permitir filtrar disciplinas que possuem tarefas em atraso.

#### Scenario: Filtro de atraso
- **WHEN** o usuário ativa o filtro de tarefas em atraso
- **THEN** o sistema retorna somente disciplinas próprias com tarefas vencidas não concluídas

### Requirement: Organize subjects by academic period
O sistema SHALL permitir associar semestre ou período a cada disciplina.

#### Scenario: Disciplina com período
- **WHEN** o usuário informa semestre ou período da disciplina
- **THEN** o sistema armazena esse valor para organização acadêmica

### Requirement: Archive completed subjects
O sistema SHALL permitir arquivar disciplinas concluídas sem excluí-las.

#### Scenario: Arquivamento de disciplina
- **WHEN** o usuário arquiva uma disciplina concluída
- **THEN** o sistema mantém a disciplina armazenada e remove da lista de disciplinas ativas

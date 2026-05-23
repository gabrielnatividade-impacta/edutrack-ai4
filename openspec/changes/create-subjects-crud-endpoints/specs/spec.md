# create-subjects-crud-endpoints Specification

## Purpose
Definir os requisitos para os endpoints CRUD de `subjects` com controle de acesso por usuário.

## ADDED Requirements
### Requirement: Create subject endpoint
The system SHALL allow authenticated users to create a new subject.
#### Scenario: User creates a subject
- **WHEN** an authenticated user submits a new subject
- **THEN** the system stores it with `user_id` igual ao usuário autenticado

### Requirement: List subjects endpoint
The system SHALL return only subjects belonging to the authenticated user.
#### Scenario: User lists subjects
- **WHEN** an authenticated user requests the subjects list
- **THEN** the system returns only subjects com `user_id` igual ao usuário autenticado

### Requirement: Update subject endpoint
The system SHALL allow updates only on subjects owned by the authenticated user.
#### Scenario: User updates own subject
- **WHEN** an authenticated user updates a subject they own
- **THEN** the system updates the subject

### Requirement: Delete subject endpoint
The system SHALL allow deletion only on subjects owned by the authenticated user.
#### Scenario: User deletes own subject
- **WHEN** an authenticated user deletes a subject they own
- **THEN** the system removes the subject
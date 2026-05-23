# create-subjects-table Design

## Solution Overview
Criar tabela subjects com relacionamento 1:N com users.

## Tables
- subjects: id (uuid, PK), name (text), code (text?), description (text?), status (text, default "active"), user_id (FK to users), account_id (FK to accounts?), created_at (timestamp), updated_at (timestamp)

## Relationships
- subjects.user_id -> users.id
- subjects.account_id -> accounts.id (opcional)
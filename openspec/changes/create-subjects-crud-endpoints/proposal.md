# Change: create-subjects-crud-endpoints

## Why
Criar endpoints CRUD para a tabela `subjects`, garantindo que cada usuário só acesse e gerencie suas próprias disciplinas.

## What Changes
- Adicionar APIs REST para `subjects`: POST, GET, PATCH e DELETE.
- Implementar controle de acesso baseado em `user_id` autenticado.

## Impact
- Usuários poderão criar, listar, atualizar e remover apenas suas disciplinas.
- Melhora a segurança e prepara a API para integração com o frontend Streamlit.
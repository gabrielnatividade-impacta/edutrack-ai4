## 1. Banco de dados

- [x] Criar tabela `subjects` no banco de dados
- [x] Adicionar campos à tabela `subjects`: `id`, `user_id`, `name`, `code`, `semester`, `description`, `created_at`, `updated_at`
- [x] Criar relacionamento entre `subjects.user_id` e `user.id`
- [x] Adicionar índice em `user_id` para buscas rápidas de matérias por usuário
- [x] Adicionar restrição única em `(user_id, code)` para evitar códigos duplicados por usuário

## 2. Validação de dados

- [x] Validar campos obrigatórios `name` e `code` na criação e atualização
- [x] Validar comprimento máximo de `code` (20 caracteres)
- [x] Garantir que `user_id` não possa ser modificado via atualização

## 3. Controle de acesso

- [x] Implementar autenticação em todos os endpoints de `subjects`
- [x] Garantir que apenas o dono da matéria possa visualizar, atualizar ou excluir o registro
- [x] Retornar 404 Not Found para tentativas de acesso a matérias de outros usuários

## 4. API e documentação

- [x] Documentar endpoints de CRUD de matérias
- [x] Definir respostas e códigos HTTP esperados (201, 400, 401, 404, 204)

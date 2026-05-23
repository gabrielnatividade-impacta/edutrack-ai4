# create-subjects-crud-endpoints Design

## Solution Overview
Implementar endpoints REST para a tabela `subjects` com autenticação e filtro por `user_id`.

## Endpoints
- POST `/subjects` - cria nova disciplina para o usuário autenticado.
- GET `/subjects` - lista disciplinas do usuário autenticado.
- PATCH `/subjects/{id}` - atualiza disciplina somente se pertencer ao usuário.
- DELETE `/subjects/{id}` - remove disciplina somente se pertencer ao usuário.

## Segurança
- Todos os endpoints exigem autenticação.
- Todas as consultas e alterações filtram `user_id == $auth.id` no Xano.
- PATCH e DELETE verificam a propriedade do registro antes de executar.
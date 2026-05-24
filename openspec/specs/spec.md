## Requisitos Formais

1. O sistema deve armazenar dados de matérias (`subjects`) em uma tabela persistente.
2. O sistema deve associar cada matéria a um usuário proprietário por meio do campo `user_id`.
3. Apenas o usuário autenticado que é proprietário de uma matéria deve poder acessar, modificar ou excluir essa matéria.
4. O campo `user_id` em `subjects` deve referenciar a entidade `user` para garantir a associação adequada entre matéria e usuário.

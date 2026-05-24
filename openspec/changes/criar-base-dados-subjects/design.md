## Contexto

Os usuários precisam de um local para registrar e gerenciar suas disciplinas acadêmicas dentro da plataforma. A implementação deve ser simples, garantir propriedade por usuário e permitir futura expansão para recursos como notas, tarefas e automações por matéria.

## Decisões

- Usar uma tabela `subjects` com chave estrangeira `user_id` para `user.id`.
- Implementar controle de acesso no nível da API, verificando se `subjects.user_id == $auth.id`.
- Manter o modelo de dados enxuto: `id`, `user_id`, `name`, `code`, `semester`, `description`, timestamps.
- Garantir unicidade do campo `code` por usuário para evitar duplicatas de disciplinas dentro da mesma conta.

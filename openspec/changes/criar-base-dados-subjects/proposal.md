## Proposta

Criar a base de dados para `subjects` de modo que cada usuário possa registrar e gerenciar suas disciplinas acadêmicas com propriedade definida. Isso viabiliza controles de acesso baseados em dono e prepara a plataforma para futuras automações relacionadas a matérias.

## O que será feito

- Criar a tabela `subjects` para armazenar disciplinas acadêmicas.
- Associar cada disciplina a um usuário proprietário via `user_id`.
- Proteger as operações de CRUD para que apenas o usuário dono possa acessar ou modificar suas próprias disciplinas.
- Validar os campos obrigatórios e a unicidade de código por usuário.

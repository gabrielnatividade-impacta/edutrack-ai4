# Xano Manual Publish Checklist

Este projeto ja esta configurado para chamar disciplinas e tarefas no API group:

`https://x8ki-letl-twmt.n7.xano.io/api:UnGtERdd`

Se o app mostrar `Endpoint /subjects nao encontrado no Xano`, significa que os arquivos locais ainda nao foram publicados no Xano. Publique manualmente os itens abaixo no API group `Members & Accounts`.

## Disciplinas

Arquivos locais que precisam existir no Xano:

- `apis/members_accounts/3600113_subjects_POST.xs` -> `POST /subjects`
- `apis/members_accounts/3600114_subjects_list_GET.xs` -> `GET /subjects`
- `apis/members_accounts/3600115_subjects_detail_GET.xs` -> `GET /subjects/{subject_id}`
- `apis/members_accounts/3600116_subjects_detail_PATCH.xs` -> `PATCH /subjects/{subject_id}`
- `apis/members_accounts/3600117_subjects_detail_DELETE.xs` -> `DELETE /subjects/{subject_id}`

Tabela usada:

- `tables/803740_subject.xs`

## Tarefas

Arquivos locais que precisam existir no Xano:

- `apis/members_accounts/tasks_GET.xs` -> `GET /tasks`
- `apis/members_accounts/tasks_POST.xs` -> `POST /tasks`
- `apis/members_accounts/tasks_id_PUT.xs` -> `PUT /tasks/{id}`
- `apis/members_accounts/tasks_id_DELETE.xs` -> `DELETE /tasks/{id}`
- `apis/members_accounts/tasks_id_complete_PATCH.xs` -> `PATCH /tasks/{id}/complete`

Tabela usada:

- `tables/840315_academic_task.xs`

## Configuracao Streamlit

O arquivo `.streamlit/secrets.toml` deve conter:

```toml
XANO_AUTH_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:X3MV-cHe"
XANO_MEMBERS_ACCOUNTS_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:UnGtERdd"
XANO_SUBJECTS_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:UnGtERdd"
XANO_TASKS_BASE_URL = "https://x8ki-letl-twmt.n7.xano.io/api:UnGtERdd"
```

## Como validar depois de publicar

1. Reinicie o Streamlit.
2. Entre no app.
3. Abra `Disciplinas`.
4. Se a tela listar vazio sem aviso de endpoint ausente, o `GET /subjects` foi encontrado.
5. Cadastre uma disciplina.
6. Abra `Tarefas`.
7. Cadastre uma tarefa vinculada a disciplina.

Nao execute push/sync/deploy automatico por agente. A publicacao no Xano deve ser feita manualmente pelo desenvolvedor.

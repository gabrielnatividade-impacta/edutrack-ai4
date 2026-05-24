## Context

O EduTrack AI possui tabelas existentes: `users` (com `user_type` para distinguir professores), `subjects`, `academic_tasks` e relacionamentos estabelecidos. Professores precisam de uma forma centralizada para lançar notas de forma controlada, com rastreamento de quem lançou e quando.

Sistema atual:
- Tabela `users` com campo `user_type` para identificar professores
- Tabela `academic_tasks` para atividades acadêmicas
- Relacionamento entre usuários e disciplinas via `subject_user` (implícito ou explícito)

Restrições:
- Apenas usuários autenticados com role `teacher` podem lançar notas
- Notas devem estar vinculadas a uma atividade específica e a um aluno
- Auditoria: registrar quem lançou a nota e quando

## Goals / Non-Goals

**Goals:**
- Criar estrutura de dados para armazenar notas (grades) de atividades por aluno
- Implementar API POST para lançamento de notas com validação de permissões
- Garantir que apenas professores da disciplina possam lançar notas para seus alunos
- Rastrear quem lançou a nota e quando (auditoria)

**Non-Goals:**
- Listar/consultar notas (GET APIs) - fora do escopo desta feature
- Atualizar ou deletar notas existentes - será feito em feature posterior se necessário
- Cálculo automático de média - responsabilidade da aplicação frontend/Streamlit
- Relatórios de notas - fora do escopo

## Decisions

### 1. Estrutura da Tabela `activity_grades`
**Decision**: Criar tabela com campos: `id`, `activity_id` (FK), `student_id` (FK), `grade` (decimal), `teacher_id` (FK), `created_at`, `updated_at`

**Rationale**: 
- Normalizado e clara rastreabilidade (quem lançou, quando, para qual atividade/aluno)
- Permite auditoria e histórico de mudanças futuro
- Évita duplicação e mantém integridade referencial

**Alternatives considered**:
- Armazenar em JSON dentro de `academic_tasks` → Difícil auditar, menos escalável
- Sem rastrear `teacher_id` → Perderíamos auditoria

### 2. Autenticação e Autorização
**Decision**: Endpoint POST requer autenticação (via Xano auth) e validação que usuário é professor da disciplina que contém a atividade

**Rationale**:
- Segurança: impede alunos lançarem notas
- Controle: professores só lançam notas em suas próprias disciplinas
- Auditoria automática via `teacher_id`

**Alternatives considered**:
- Permitir qualquer professor lançar em qualquer atividade → Risco de segurança
- Sem validação de permissão → Integridade comprometida

### 3. Validação de Entrada
**Decision**: Validar que `grade` está entre 0 e 10 (ou escala definida), `student_id` existe e é aluno, `activity_id` existe e pertence à disciplina do professor

**Rationale**:
- Previne dados inválidos no banco
- Feedback útil ao usuário (mensagens de erro claras)

### 4. Resposta da API
**Decision**: POST retorna objeto criado com `id`, `activity_id`, `student_id`, `grade`, `created_at`

**Rationale**:
- Confirma ao cliente que foi salvo
- Permite exibir feedback visual (frontend/Streamlit)

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Professor lança nota incorreta sem poder corrigi-la | Adicionar UPDATE API em feature futura. Por enquanto, documentar que professor deve revisar antes de enviar. |
| Múltiplos professores tentam lançar nota para mesmo aluno/atividade | Unique constraint em `(activity_id, student_id)` previne duplicação; posterior tentativa retorna erro 409 Conflict. |
| Performance: muitas grades para uma atividade | Adicionar índice em `(activity_id, student_id)`. Paginação será adicionada em relatórios futuros. |
| Segurança: professor lança nota fora de sua disciplina | Validação de `teacher_id` vs `activity.subject_id` previne. Teste de integração crítico. |

## Migration Plan

**Deployment**:
1. Criar tabela `activity_grades` no Xano
2. Deploy API endpoint POST `/academic_tasks/{task_id}/grades`
3. Testar manualmente (seção testing em tasks.md)
4. Comunicar aos professores a nova funcionalidade via Streamlit

**Rollback** (se necessário):
- Remover endpoint da API group
- Tabela permanece (dados preservados para futura recuperação)
- Nenhum impacto em features existentes

## Open Questions

- Qual é a escala de notas? (0-10, 0-100, A-F) → Será definido em spec.md `activity-grades`
- Permitir atualizar nota já lançada? → Scope para feature futura; por enquanto POST-only
- Integração com relatórios de notas no Streamlit? → Fora do escopo desta feature

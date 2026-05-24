# Implementar Checklist EduTrack AI v2

## Why
O EduTrack AI já possui partes de autenticação, disciplinas e tarefas, mas o checklist funcional mostra que ainda faltam fluxos completos, integração consistente com o Xano, telas de progresso, relatórios, exportação e melhorias de experiência. Além disso, o push de APIs para o Xano está falhando por inconsistências nos arquivos `.xs`, incluindo conflitos Git em endpoints de disciplinas.

## What Changes
- Corrigir arquivos XanoScript de APIs de disciplinas que impedem o push local para o Xano.
- Completar autenticação e acesso com cadastro, login, sessão persistente, perfil, redefinição de senha e expiração de token.
- Completar CRUD de disciplinas com vínculo ao usuário, prevenção de duplicidade, busca, filtro de atraso, semestre/período e arquivamento.
- Completar CRUD de tarefas com vínculo à disciplina e ao usuário, status, prioridade, agrupamentos, filtros e sinalização de atraso.
- Criar dashboard pós-login com totais, próximas tarefas e progresso geral.
- Criar relatórios com histórico por período, progresso por disciplina e exportação CSV/PDF.
- Melhorar identidade visual, telas de login/cadastro, estado vazio e confirmações antes de exclusão.

## Impact
- Backend Xano: tabelas, APIs e possivelmente funções auxiliares para autenticação, disciplinas, tarefas, relatórios e exportação.
- Frontend Streamlit: novas telas e ajustes de navegação para dashboard, disciplinas, tarefas, perfil e relatórios.
- OpenSpec: deltas para autenticação, disciplinas, tarefas, dashboard, relatórios e experiência do usuário.
- Não inclui push, sync ou deploy para Xano; o desenvolvedor fará essa etapa manualmente.

## Context

EduTrack currently has a user authentication system and event logging, but no way for users to manage their academic subjects/courses. The event logging system is already in place for audit trails. We have established APIs for authentication and event management. We're building on existing patterns using XanoScript for database queries and API endpoints.

## Goals / Non-Goals

**Goals:**
- Enable users to create and manage a list of their academic subjects
- Implement ownership-based access control (users can only manage their own subjects)
- Support subject metadata (code, name, semester, description, academic period)
- Create audit trail for all subject operations
- Establish the foundation for subject-dependent features (assignments, grades, attendance)

**Non-Goals:**
- Role-based access (e.g., instructor vs student) - initial implementation focused on ownership only
- Subject templates or sharing between users
- Subject scheduling or calendar integration
- Batch import of subjects from institutional systems
- Subject prerequisites or dependencies tracking

## Decisions

**Decision 1: Flat subjects table with user ownership**
- Subject data stored in a single `subjects` table with `user_id` foreign key to enforce ownership
- Each user owns their subjects; no sharing in v1
- **Why**: Simple, fast iteration. Sharing can be added later if needed.
- **Alternatives**: (1) Shared subjects with explicit permission matrix - too complex for current needs; (2) Multi-tenant subject groups - premature optimization

**Decision 2: Ownership-based access control at API level**
- Authentication required for all subject endpoints; authorization checks that `user_id` in record matches authenticated user
- No database-level roles; business logic in API handlers
- **Why**: Aligns with existing auth patterns; easy to test and debug
- **Alternatives**: (1) Database-level row security - adds infrastructure complexity; (2) Token-scoped access - requires significant refactor

**Decision 3: Subject operations logged to event_log automatically**
- Each create/update/delete triggers `log_event` function with action="subject_created|updated|deleted"
- Async logging (fire-and-forget) to avoid blocking subject operations
- **Why**: Reuses existing event system; provides audit trail without new infrastructure
- **Alternatives**: (1) Separate audit table - redundant with event system; (2) No logging - loses audit trail

**Decision 4: Minimal subject metadata in v1**
- Fields: id, user_id, name, code, semester, created_at, updated_at
- Description as optional; no instructor, room, or schedule info
- **Why**: MVP focus on core CRUD; additional fields trivial to add later
- **Alternatives**: (1) Full academic metadata now - over-engineering; (2) No code field - limits integration with other systems

## Risks / Trade-offs

**Risk 1: N+1 queries when listing subjects with user info**
→ Mitigation: API returns only subject data; if frontend needs user info, it's already authenticated (cached session data available client-side)

**Risk 2: No notification when other users share/assign a subject to the original owner**
→ Mitigation: Out of scope for v1; notification system can be added when sharing feature requested

**Risk 3: Soft delete not implemented; deleted subjects are permanently removed**
→ Mitigation: Event log preserves deletion records; can restore from backups if needed. Hard delete acceptable for MVP.

**Risk 4: Concurrent updates to same subject could cause conflicts**
→ Mitigation: Accept last-write-wins; Xano handles this with transaction timestamps. Can add optimistic locking in v2 if conflicts become problem.

## Migration Plan

**Deployment:**
1. Create `subjects` table schema in Xano
2. Create API endpoints for subject CRUD
3. Deploy event logging integration
4. Test with manual scenarios
5. Release as beta feature

**Rollback:**
- If critical issues found: disable subject APIs via feature flag (if available), keep table intact for diagnostics
- Data recovery: restore from backup if corruption occurs
- No data migration needed (new table)

## Open Questions

- Should subjects have a visibility setting (private/shared/public) for future v2 sharing feature?
- Do we need to track subject instructors or just ownership?
- Should there be a "default" subject selected for new users?
- Should deleted subjects be soft-deleted with archival capability?

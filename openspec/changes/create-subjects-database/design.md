## Context

The edutrack-ai4 platform currently has user and account management infrastructure with role-based access control. Users can be members of accounts and have different roles (owner, admin, member, guest). The system needs to extend this to support subjects/disciplines, which are a core entity in educational management. Each subject will be associated with an account and managed by users with appropriate permissions.

**Current State:**
- Account-based organization exists with user roles
- Role-based access control (RBAC) system is implemented via the `role_based_access_control` function
- Event logging system tracks account-level activities
- User management API endpoints support team member management

**Stakeholders:**
- Users: Need to organize and manage their subjects
- Account admins: Need to control who can manage which subjects
- System: Needs to support future automations based on subject data

## Goals / Non-Goals

**Goals:**
- Create a robust `subject` database table that stores disciplinary information
- Enable account-level subject management with proper foreign key relationships
- Prepare the data model for future subject-level access control and automation
- Maintain consistency with existing account/user relationship patterns
- Support metadata extensibility for future academic properties

**Non-Goals:**
- Implement subject-level API endpoints (will be done in a separate task/change)
- Create UI for subject management (frontend development - separate phase)
- Implement subject-level event logging (can be added later if needed)
- Support complex subject scheduling or conflicts (out of scope)
- Implement automatic enrollment or registration workflows (future feature)

## Decisions

### 1. Account-Level Subject Association (vs User-Level)

**Decision:** Subjects are owned by accounts, not individual users.

**Rationale:**
- Aligns with existing architecture where accounts are the organizational unit
- Enables team collaboration on subjects
- Supports future role-based subject access (admins can manage all account subjects)
- Simpler to implement and maintain

**Alternative Considered:**
- User-level ownership: More granular but creates complexity for team-shared subjects and would require additional join tables for multi-user access

### 2. Required vs Optional Fields

**Decision:** Include essential academic fields (code, credits, semester) with clear purposes; allow optional fields for extensibility.

**Rationale:**
- Essential fields (name, code, description) are universally required for subject identification
- Academic fields (credits, semester, year) support transcript and schedule features
- Optional fields (color, icon, tags) enable UI customization without schema changes
- Timestamps (created_at, updated_at) support audit trails and sorting

### 3. Status/State Field

**Decision:** Include an `is_active` boolean flag for soft deletion and status tracking.

**Rationale:**
- Allows archiving subjects without data loss
- Supports historical tracking of past subjects
- Simpler than complex status enums for initial implementation
- Can be extended to a status enum in the future if needed

### 4. Relationship Integrity

**Decision:** Use foreign key constraint to `account` table with cascade delete.

**Rationale:**
- Maintains referential integrity - subjects cannot exist without an account
- When account is deleted, associated subjects are automatically removed
- Prevents orphaned subject records
- Database enforces the relationship rule

## Risks / Trade-offs

- **Risk:** N+1 query problem if subjects are always loaded with account data
  - **Mitigation:** Create database addons for efficient subject queries with account filtering; encourage pagination on list endpoints

- **Risk:** Schema evolution if new academic fields are needed
  - **Mitigation:** Include optional fields early; plan for future schema migrations; consider using JSON columns for flexible metadata

- **Risk:** Performance impact if account has many subjects
  - **Mitigation:** Add database indexes on account_id and is_active fields; plan for pagination in API endpoints

- **Risk:** Access control bypass if RBAC is not properly integrated with subject operations
  - **Mitigation:** Subject APIs must integrate with existing role_based_access_control function; enforce account membership check before subject access

## Migration Plan

### Deployment Steps

1. **Create the `subject` table** with all fields defined in specs
2. **Add database indexes** on account_id, is_active, created_at for query performance
3. **Verify referential integrity** by testing cascade delete behavior
4. **Document the schema** for API documentation and developer reference
5. **Prepare for future APIs** - ensure table is ready to support CRUD endpoints

### Rollback Strategy

- If issues are discovered, the `subject` table can be dropped without affecting other tables (it only has a foreign key to `account`, no other tables depend on it)
- No data migration or backward compatibility concerns since this is a new table

## Open Questions

- Should subjects support cross-account visibility for collaboration scenarios? (Defer to future capability)
- Will subjects need to track academic credits for GPA calculations? (Yes, include as optional field for future use)
- Should we implement soft delete via status field or hard delete with archival table? (Using soft delete with is_active flag - revisit if archival needs become complex)
